import random
import copy
import time


class GeneticAlgorithm:
    def __init__(self, maze, params=None):
        # Inicializa GA com parâmetros padrão
        self.maze = maze
        
        default_params = {
            'TAMANHO_POPULACAO': 100,
            'TAXA_MUTACAO': 0.01,
            'TAXA_CROSSOVER': 0.8,
            'NUM_GERACOES': 10,
            'TAMANHO_CROMOSSOMO': max(50, (maze.n * maze.n) // 2),
            'TORNEIO_SIZE': 3,
            'VERBOSE': True,
            'VERBOSE_INTERVAL': 1,
            'VERBOSE_DETAIL': True,
            'MODO_LENTO': False,
            'DELAY_GERACAO': 0.5,
            'PAUSAR_A_CADA': 0,
            'ANALISE_CONVERGENCIA': False,
            'SHOW_ELITISM': False,
            'TRACK_HISTORY': False,
            'TRACK_FULL_POPULATION': False,
            'SHOW_POPULATION': 0,
            'TRACK_PHASES': False,
        }
        
        if params:
            default_params.update(params)
        
        self.params = default_params
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.diversity_history = []
        self.generation_found = None
        self.s_position = None
        self.generation_details = []
        self.phase_logs = []
    
    def create_random_chromosome(self):
        # Cria cromossomo aleatório (sequência de movimentos 0-7)
        return [random.randint(0, 7) for _ in range(self.params['TAMANHO_CROMOSSOMO'])]
    
    def evaluate_fitness(self, chromosome):
        # Avalia aptidão: retorna (fitness, posição_final, caminho)
        linha, coluna = self.maze.pos_E
        path = [(linha, coluna)]
        visited_cells = {(linha, coluna)}
        
        for direction in chromosome:
            result = self.maze.move(linha, coluna, direction)
            
            if result is None:
                continue
            
            linha, coluna = result
            path.append((linha, coluna))
            visited_cells.add((linha, coluna))
            
            if self.maze.get_cell(linha, coluna) == 'S':
                BASE_SUCCESS = 10000.0
                efficiency_bonus = 1000.0 / len(path)
                return BASE_SUCCESS + efficiency_bonus, (linha, coluna), path
        
        linha_entrada, coluna_entrada = self.maze.pos_E
        linha_saida, coluna_saida = self.maze.pos_S
        
        # Distância do ponto final até a saída (quanto menor, melhor)
        distance_to_exit = abs(linha - linha_saida) + abs(coluna - coluna_saida)
        
        # Quanto mais células únicas exploradas, melhor
        exploration_bonus = len(visited_cells) * 10.0
        
        # Penalidade por estar longe da saída
        distance_penalty = distance_to_exit * 5.0
        
        # Bônus por ter se movido (não ficar parado)
        movement_bonus = len(path) * 0.5
        
        # Fitness final
        fitness = exploration_bonus + movement_bonus - distance_penalty
        
        # Evitar fitness negativo (mínimo 0.1 para cromossomos que exploram mas não acham S)
        fitness = max(0.1, fitness)
        
        return fitness, (linha, coluna), path
    
    def tournament_selection(self, population, fitnesses):
        # Seleção por torneio
        tournament_size = self.params['TORNEIO_SIZE']
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        
        # Retornar o melhor do torneio
        return max(tournament, key=lambda x: x[1])[0]
    
    def crossover(self, parent1, parent2):
        # Crossover de um ponto
        if random.random() > self.params['TAXA_CROSSOVER']:
            # Sem crossover, retornar cópias dos pais
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Ponto de corte aleatório
        point = random.randint(1, len(parent1) - 1)
        
        # Criar filhos
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        return child1, child2
    
    def mutate(self, chromosome):
        # Mutação: altera genes aleatoriamente
        mutated = copy.deepcopy(chromosome)
        
        for i in range(len(mutated)):
            if random.random() < self.params['TAXA_MUTACAO']:
                mutated[i] = random.randint(0, 7)
        
        return mutated
    
    def calculate_diversity(self, population):
        # Calcula diversidade genética da população (0-1)
        if len(population) < 2:
            return 0.0
        
        # Amostrar alguns cromossomos para eficiência
        sample_size = min(20, len(population))
        sample = random.sample(population, sample_size)
        
        # Calcular diferenças médias entre cromossomos
        total_diff = 0
        comparisons = 0
        
        for i in range(len(sample)):
            for j in range(i + 1, len(sample)):
                # Contar genes diferentes
                diff = sum(1 for k in range(len(sample[i])) if sample[i][k] != sample[j][k])
                total_diff += diff
                comparisons += 1
        
        if comparisons == 0:
            return 0.0
        
        # Normalizar pela diversidade máxima possível
        avg_diff = total_diff / comparisons
        max_diff = len(population[0])  # Tamanho do cromossomo
        
        return avg_diff / max_diff if max_diff > 0 else 0.0
    
    def detect_convergence(self, fitness_history, window=20):
        # Detecta convergência prematura
        if len(fitness_history) < window:
            return False
        
        recent = fitness_history[-window:]
        
        # Se o fitness não mudou nas últimas 'window' gerações
        if len(set(recent)) == 1:
            return True
        
        # Se a variação é muito pequena
        variation = max(recent) - min(recent)
        if variation < 0.01:
            return True
        
        return False
    
    def run(self):
        # Executa o AG até encontrar S ou atingir máximo de gerações
        # Mostrar informações iniciais
        if self.params['VERBOSE']:
            print(f"\n{'='*60}")
            print(f"INICIANDO ALGORITMO GENETICO")
            print(f"{'='*60}")
            print(f"Parametros:")
            print(f"   - Tamanho da Populacao: {self.params['TAMANHO_POPULACAO']}")
            print(f"   - Tamanho do Cromossomo: {self.params['TAMANHO_CROMOSSOMO']} movimentos")
            print(f"   - Taxa de Mutacao: {self.params['TAXA_MUTACAO']*100}%")
            print(f"   - Taxa de Crossover: {self.params['TAXA_CROSSOVER']*100}%")
            print(f"   - Geracoes Maximas: {self.params['NUM_GERACOES']}")
            print(f"   - Tamanho do Torneio: {self.params['TORNEIO_SIZE']}")
            print(f"Objetivo: Encontrar a saida 'S' do labirinto {self.maze.n}x{self.maze.n}")
            print(f"   Partindo de E = {self.maze.pos_E}")
            print(f"{'='*60}\n")
        
        # FASE 0: Criar população inicial
        population = [self.create_random_chromosome() 
                      for _ in range(self.params['TAMANHO_POPULACAO'])]
        
        if self.params.get('TRACK_PHASES', False):
            self.phase_logs.append({
                'generation': 0,
                'phase': 'INICIALIZAÇÃO',
                'description': 'População inicial criada aleatoriamente',
                'details': {
                    'population_size': len(population),
                    'chromosome_length': self.params['TAMANHO_CROMOSSOMO'],
                    'method': 'Geração aleatória de movimentos (0-7)'
                }
            })
        
        best_ever_chromosome = None
        best_ever_fitness = 0
        best_ever_position = None
        best_ever_path = None
        
        for generation in range(self.params['NUM_GERACOES']):
            # FASE 1: Avaliar fitness de toda a população
            fitness_results = [self.evaluate_fitness(chromo) for chromo in population]
            fitnesses = [f[0] for f in fitness_results]
            
            if self.params.get('TRACK_PHASES', False):
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'AVALIAÇÃO DE FITNESS',
                    'description': 'Cada cromossomo é avaliado (simulação no labirinto)',
                    'details': {
                        'total_evaluations': len(fitnesses),
                        'best_fitness': max(fitnesses),
                        'avg_fitness': sum(fitnesses) / len(fitnesses),
                        'worst_fitness': min(fitnesses),
                        'valid_paths': sum(1 for f in fitnesses if f > 0)
                    }
                })
            
            # FASE 2: Encontrar o melhor desta geração
            best_idx = fitnesses.index(max(fitnesses))
            best_fitness = fitnesses[best_idx]
            best_chromosome = population[best_idx]
            best_position = fitness_results[best_idx][1]
            best_path = fitness_results[best_idx][2]
            
            if self.params.get('TRACK_PHASES', False):
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'IDENTIFICAÇÃO DO MELHOR',
                    'description': 'Melhor indivíduo da geração identificado',
                    'details': {
                        'best_individual_id': best_idx,
                        'fitness': best_fitness,
                        'position': best_position,
                        'path_length': len(best_path),
                        'found_exit': best_fitness >= 10000.0
                    }
                })
            
            # FASE 3: Atualizar melhor global (Elitismo)
            elite_preserved = False
            if best_fitness > best_ever_fitness:
                best_ever_fitness = best_fitness
                best_ever_chromosome = copy.deepcopy(best_chromosome)
                best_ever_position = best_position
                best_ever_path = best_path
                elite_preserved = False  # Novo melhor encontrado
            else:
                elite_preserved = True  # Elite anterior preservado
            
            if self.params.get('TRACK_PHASES', False):
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'ELITISMO',
                    'description': 'Melhor indivíduo global é preservado para próxima geração',
                    'details': {
                        'elite_fitness': best_ever_fitness,
                        'status': 'Preservado da geração anterior' if elite_preserved else 'Novo melhor encontrado',
                        'elite_will_survive': True
                    }
                })
            
            # Calcular métricas
            avg_fitness = sum(fitnesses) / len(fitnesses)
            diversity = self.calculate_diversity(population)
            
            self.best_fitness_history.append(best_ever_fitness)
            self.avg_fitness_history.append(avg_fitness)
            self.diversity_history.append(diversity)
            
            # Rastrear histórico completo se solicitado
            if self.params.get('TRACK_HISTORY', False):
                valid_paths = sum(1 for f in fitnesses if f > 0)
                min_fitness = min(fitnesses)
                max_fitness = max(fitnesses)
                
                generation_data = {
                    'generation': generation,
                    'best_fitness_generation': best_fitness,
                    'best_fitness_global': best_ever_fitness,
                    'avg_fitness': avg_fitness,
                    'min_fitness': min_fitness,
                    'max_fitness': max_fitness,
                    'diversity': diversity,
                    'valid_paths': valid_paths,
                    'total_population': len(population),
                    'best_position': best_position,
                    'path_length': len(best_path)
                }
                
                # Rastrear população completa se solicitado
                if self.params.get('TRACK_FULL_POPULATION', False):
                    population_data = []
                    for i, (chromo, (fit, pos, path)) in enumerate(zip(population, fitness_results)):
                        population_data.append({
                            'id': i,
                            'fitness': fit,
                            'position': pos,
                            'path_length': len(path),
                            'unique_cells': len(set(path))
                        })
                    generation_data['population'] = population_data
                
                self.generation_details.append(generation_data)
            
            # Verificar se encontrou a solução
            # Fitness >= 10000.0 indica que a saída foi encontrada
            if best_fitness >= 10000.0:
                self.generation_found = generation
                self.s_position = best_position
                
                if self.params['VERBOSE']:
                    print(f"\n{'='*60}")
                    print(f"SAIDA ENCONTRADA!")
                    print(f"{'='*60}")
                    print(f"   Geracao: {generation}")
                    print(f"   Posicao da Saida: {best_position}")
                    print(f"   Tamanho do Caminho: {len(best_ever_path)} passos")
                    print(f"{'='*60}\n")
                
                return {
                    'success': True,
                    'generation': generation,
                    's_position': best_position,
                    'chromosome': best_ever_chromosome,
                    'path': best_ever_path,
                    'fitness': best_ever_fitness,
                    'best_fitness_history': self.best_fitness_history,
                    'avg_fitness_history': self.avg_fitness_history,
                    'diversity_history': self.diversity_history,
                    'generation_details': self.generation_details,
                    'phase_logs': self.phase_logs
                }
            
            # Log de progresso
            if self.params['VERBOSE'] and (generation % self.params['VERBOSE_INTERVAL'] == 0 or generation == 0):
                print(f"\n{'-'*60}")
                print(f"GERACAO {generation}")
                print(f"{'-'*60}")
                print(f"  Melhor Fitness da Geracao: {best_fitness:.2f}")
                print(f"  Melhor Fitness Global: {best_ever_fitness:.2f}")
                print(f"  Posicao Final: {best_position}")
                
                # Visualização de elitismo
                if self.params.get('SHOW_ELITISM', False):
                    if generation > 0:
                        status = "[ELITE PRESERVADO]" if best_ever_fitness == self.best_fitness_history[-2] else "[NOVO MELHOR]"
                        print(f"  Elitismo: {status}")
                
                # Mostrar população completa ou top N
                show_pop = self.params.get('SHOW_POPULATION', 0)
                if show_pop > 0:
                    print(f"\n  Top {show_pop} Individuos desta Geracao:")
                    print(f"  {'ID':<5} {'Fitness':<15} {'Posicao Final':<20} {'Passos':<8} {'Celulas Unicas':<15}")
                    print(f"  {'-'*70}")
                    
                    # Ordenar por fitness (melhor primeiro)
                    sorted_pop = sorted(enumerate(fitness_results), key=lambda x: x[1][0], reverse=True)
                    
                    for rank, (idx, (fit, pos, path)) in enumerate(sorted_pop[:show_pop], 1):
                        unique_cells = len(set(path))
                        status = "[*] " if rank == 1 else "    "
                        print(f"  {status}{idx:<3} {fit:<15.2f} {str(pos):<20} {len(path):<8} {unique_cells:<15}")
                    
                    if show_pop < len(population):
                        print(f"  ... e mais {len(population) - show_pop} indivíduos")
                
                if self.params.get('VERBOSE_DETAIL', False):
                    # Estatísticas da população
                    valid_paths = sum(1 for f in fitnesses if f > 0)
                    print(f"  Fitness Medio: {avg_fitness:.2f}")
                    print(f"  Caminhos Validos: {valid_paths}/{len(fitnesses)}")
                    print(f"  Tamanho do Caminho: {len(best_path)} passos")
                    
                    # Análise de convergência
                    if self.params.get('ANALISE_CONVERGENCIA', False):
                        print(f"  Diversidade Genetica: {diversity:.2%}")
                        
                        if len(self.best_fitness_history) >= 10:
                            stagnation = len(self.best_fitness_history) - max((i for i, f in enumerate(self.best_fitness_history) if f != best_ever_fitness), default=0) - 1
                            print(f"  Geracoes Estagnadas: {stagnation}")
                            
                            if diversity < 0.1:
                                print(f"  ALERTA: Baixa diversidade - risco de convergência prematura!")
                            
                            if self.detect_convergence(self.best_fitness_history):
                                print(f"  ALERTA: Convergência detectada!")
                    
                    # Mostrar início do caminho
                    if len(best_path) > 1:
                        path_preview = " > ".join([f"{p}" for p in best_path[:min(5, len(best_path))]])
                        if len(best_path) > 5:
                            path_preview += " > ..."
                        print(f"  Caminho: {path_preview}")
                
                print(f"{'-'*60}")
                
                # Modo lento: adicionar delay entre gerações
                if self.params.get('MODO_LENTO', False):
                    delay = self.params.get('DELAY_GERACAO', 0.5)
                    time.sleep(delay)
                
                # Pausa interativa: esperar Enter do usuário
                pausar_a_cada = self.params.get('PAUSAR_A_CADA', 0)
                if pausar_a_cada > 0 and generation > 0 and generation % pausar_a_cada == 0:
                    input(f"\n[PAUSA] Pressione Enter para continuar (próximas {pausar_a_cada} gerações)...")
            
            # FASE 4: Criar nova população
            new_population = []
            
            # Elitismo: manter o melhor (se existir)
            if best_ever_chromosome is not None:
                new_population.append(copy.deepcopy(best_ever_chromosome))
            else:
                new_population.append(copy.deepcopy(best_chromosome))
            
            # Contadores para estatísticas
            selections_count = 0
            crossovers_count = 0
            mutations_count = 0
            genes_mutated = 0
            
            # Gerar o resto da população
            while len(new_population) < self.params['TAMANHO_POPULACAO']:
                # FASE 5: Seleção por Torneio
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)
                selections_count += 2
                
                # FASE 6: Crossover
                child1, child2 = self.crossover(parent1, parent2)
                crossovers_count += 1
                
                # FASE 7: Mutação
                child1_original = copy.deepcopy(child1)
                child2_original = copy.deepcopy(child2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                # Contar genes mutados
                genes_mutated += sum(1 for i in range(len(child1)) if child1[i] != child1_original[i])
                genes_mutated += sum(1 for i in range(len(child2)) if child2[i] != child2_original[i])
                mutations_count += 2
                
                new_population.append(child1)
                if len(new_population) < self.params['TAMANHO_POPULACAO']:
                    new_population.append(child2)
            
            if self.params.get('TRACK_PHASES', False):
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'SELEÇÃO POR TORNEIO',
                    'description': f'Pais selecionados via torneio (tamanho {self.params["TORNEIO_SIZE"]})',
                    'details': {
                        'total_selections': selections_count,
                        'tournament_size': self.params['TORNEIO_SIZE'],
                        'method': 'Seleciona melhor de K indivíduos aleatórios'
                    }
                })
                
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'CROSSOVER (RECOMBINAÇÃO)',
                    'description': 'Pais combinados para gerar filhos (crossover de um ponto)',
                    'details': {
                        'total_crossovers': crossovers_count,
                        'rate': self.params['TAXA_CROSSOVER'] * 100,
                        'method': 'One-point crossover',
                        'preserves_sequences': True
                    }
                })
                
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'MUTAÇÃO',
                    'description': 'Genes alterados aleatoriamente para manter diversidade',
                    'details': {
                        'individuals_processed': mutations_count,
                        'genes_mutated': genes_mutated,
                        'mutation_rate': self.params['TAXA_MUTACAO'] * 100,
                        'expected_mutations_per_chromosome': self.params['TAMANHO_CROMOSSOMO'] * self.params['TAXA_MUTACAO'],
                        'avg_mutations_per_individual': genes_mutated / mutations_count if mutations_count > 0 else 0
                    }
                })
                
                self.phase_logs.append({
                    'generation': generation,
                    'phase': 'NOVA GERAÇÃO FORMADA',
                    'description': 'Nova população completa (elite + filhos)',
                    'details': {
                        'population_size': len(new_population),
                        'elite_count': 1,
                        'offspring_count': len(new_population) - 1
                    }
                })
            
            population = new_population
        
        # Não encontrou solução
        if self.params['VERBOSE']:
            print(f"ERRO: Algoritmo genético não encontrou a saída após {self.params['NUM_GERACOES']} gerações.")
            print(f"Melhor fitness alcançado: {best_ever_fitness:.2f}")
        
        return {
            'success': False,
            'generation': self.params['NUM_GERACOES'],
            's_position': None,
            'chromosome': best_ever_chromosome,
            'path': best_ever_path,
            'fitness': best_ever_fitness,
            'best_fitness_history': self.best_fitness_history,
            'avg_fitness_history': self.avg_fitness_history,
            'diversity_history': self.diversity_history,
            'generation_details': self.generation_details,
            'phase_logs': self.phase_logs
        }


def run_genetic(maze, params=None):
    # Função de conveniência para executar o GA
    ga = GeneticAlgorithm(maze, params)
    return ga.run()