"""genetic.py
Breve: Implementa o ciclo do Algoritmo Genético (população, seleção, crossover, mutação).
Segunda linha: expor run_genetic(map, params) que retorna cromossomo vencedor ou None.
"""

import random
import copy
import time


class GeneticAlgorithm:
    """
    Implementa o Algoritmo Genético para descobrir a saída do labirinto.
    """
    
    def __init__(self, maze, params=None):
        """
        Inicializa o GA com parâmetros.
        
        Args:
            maze: objeto Maze
            params: dicionário com parâmetros do GA
        """
        self.maze = maze
        
        # Parâmetros padrão
        default_params = {
            'TAMANHO_POPULACAO': 100,
            'TAXA_MUTACAO': 0.01,
            'TAXA_CROSSOVER': 0.8,
            'NUM_GERACOES': 500,
            'TAMANHO_CROMOSSOMO': max(50, (maze.n * maze.n) // 2),
            'TORNEIO_SIZE': 3,
            'VERBOSE': True,
            'VERBOSE_INTERVAL': 1,  # Mostrar cada geração
            'VERBOSE_DETAIL': True,  # Mostrar detalhes extras
            'MODO_LENTO': False,     # Modo lento para visualização humana
            'DELAY_GERACAO': 0.5,    # Segundos de delay entre gerações (se MODO_LENTO=True)
            'PAUSAR_A_CADA': 0,      # Pausar e esperar Enter a cada N gerações (0=desabilitado)
            'ANALISE_CONVERGENCIA': False,  # Exibir métricas de convergência
        }
        
        if params:
            default_params.update(params)
        
        self.params = default_params
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.diversity_history = []
        self.generation_found = None
        self.s_position = None
    
    def create_random_chromosome(self):
        """
        Cria um cromossomo aleatório (sequência de movimentos).
        """
        return [random.randint(0, 7) for _ in range(self.params['TAMANHO_CROMOSSOMO'])]
    
    def evaluate_fitness(self, chromosome):
        """
        Avalia a aptidão de um cromossomo.
        
        Returns:
            tuple: (fitness, final_position, path)
        """
        # Iniciar na entrada
        linha, coluna = self.maze.pos_E
        path = [(linha, coluna)]
        visited_cells = {(linha, coluna)}
        
        # Simular cada movimento
        for direction in chromosome:
            result = self.maze.move(linha, coluna, direction)
            
            if result is None:
                # Movimento inválido (parede ou fora dos limites)
                # NÃO retornar imediatamente!
                # Simplesmente pular este movimento e tentar o próximo
                continue
            
            linha, coluna = result
            path.append((linha, coluna))
            visited_cells.add((linha, coluna))
            
            # Verificar se encontrou a saída
            if self.maze.get_cell(linha, coluna) == 'S':
                # SOLUÇÃO ENCONTRADA!
                return 1000000.0, (linha, coluna), path
        
        # Caminho válido mas não encontrou S
        # Fitness baseado em:
        # 1. Distância da entrada (incentiva exploração)
        # 2. Número de células únicas visitadas (premia diversidade)
        # 3. Proximidade à saída (bônus se chegar perto)
        
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
        """
        Seleção por torneio.
        """
        tournament_size = self.params['TORNEIO_SIZE']
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        
        # Retornar o melhor do torneio
        return max(tournament, key=lambda x: x[1])[0]
    
    def crossover(self, parent1, parent2):
        """
        Crossover de um ponto.
        """
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
        """
        Mutação: altera genes aleatoriamente baseado na taxa de mutação.
        """
        mutated = copy.deepcopy(chromosome)
        
        for i in range(len(mutated)):
            if random.random() < self.params['TAXA_MUTACAO']:
                mutated[i] = random.randint(0, 7)
        
        return mutated
    
    def calculate_diversity(self, population):
        """
        Calcula a diversidade genética da população.
        
        Returns:
            float: diversidade (0-1, onde 1 = máxima diversidade)
        """
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
        """
        Detecta convergência prematura analisando histórico de fitness.
        
        Returns:
            bool: True se convergiu prematuramente
        """
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
        """
        Executa o algoritmo genético.
        
        Returns:
            dict: resultados incluindo cromossomo vencedor, posição S, caminho, etc.
        """
        # Mostrar informações iniciais
        if self.params['VERBOSE']:
            print(f"\n{'═'*60}")
            print(f"INICIANDO ALGORITMO GENÉTICO")
            print(f"{'═'*60}")
            print(f"Parâmetros:")
            print(f"   • Tamanho da População: {self.params['TAMANHO_POPULACAO']}")
            print(f"   • Tamanho do Cromossomo: {self.params['TAMANHO_CROMOSSOMO']} movimentos")
            print(f"   • Taxa de Mutação: {self.params['TAXA_MUTACAO']*100}%")
            print(f"   • Taxa de Crossover: {self.params['TAXA_CROSSOVER']*100}%")
            print(f"   • Gerações Máximas: {self.params['NUM_GERACOES']}")
            print(f"   • Tamanho do Torneio: {self.params['TORNEIO_SIZE']}")
            print(f"\nObjetivo: Encontrar a saída 'S' do labirinto {self.maze.n}x{self.maze.n}")
            print(f"   Partindo de E = {self.maze.pos_E}")
            print(f"{'═'*60}\n")
        
        # Criar população inicial
        population = [self.create_random_chromosome() 
                      for _ in range(self.params['TAMANHO_POPULACAO'])]
        
        best_ever_chromosome = None
        best_ever_fitness = 0
        best_ever_position = None
        best_ever_path = None
        
        for generation in range(self.params['NUM_GERACOES']):
            # Avaliar fitness de toda a população
            fitness_results = [self.evaluate_fitness(chromo) for chromo in population]
            fitnesses = [f[0] for f in fitness_results]
            
            # Encontrar o melhor desta geração
            best_idx = fitnesses.index(max(fitnesses))
            best_fitness = fitnesses[best_idx]
            best_chromosome = population[best_idx]
            best_position = fitness_results[best_idx][1]
            best_path = fitness_results[best_idx][2]
            
            # Atualizar melhor global
            if best_fitness > best_ever_fitness:
                best_ever_fitness = best_fitness
                best_ever_chromosome = copy.deepcopy(best_chromosome)
                best_ever_position = best_position
                best_ever_path = best_path
            
            # Calcular métricas
            avg_fitness = sum(fitnesses) / len(fitnesses)
            diversity = self.calculate_diversity(population)
            
            self.best_fitness_history.append(best_ever_fitness)
            self.avg_fitness_history.append(avg_fitness)
            self.diversity_history.append(diversity)
            
            # Verificar se encontrou a solução
            if best_fitness >= 1000000.0:
                self.generation_found = generation
                self.s_position = best_position
                
                if self.params['VERBOSE']:
                    print(f"\n{'═'*60}")
                    print(f"SAÍDA ENCONTRADA!")
                    print(f"{'═'*60}")
                    print(f"   Geração: {generation}")
                    print(f"   Posição da Saída: {best_position}")
                    print(f"   Tamanho do Caminho: {len(best_ever_path)} passos")
                    print(f"{'═'*60}\n")
                
                return {
                    'success': True,
                    'generation': generation,
                    's_position': best_position,
                    'chromosome': best_ever_chromosome,
                    'path': best_ever_path,
                    'fitness': best_ever_fitness,
                    'best_fitness_history': self.best_fitness_history,
                    'avg_fitness_history': self.avg_fitness_history,
                    'diversity_history': self.diversity_history
                }
            
            # Log de progresso
            if self.params['VERBOSE'] and (generation % self.params['VERBOSE_INTERVAL'] == 0 or generation == 0):
                print(f"\n{'─'*60}")
                print(f"GERAÇÃO {generation}")
                print(f"{'─'*60}")
                print(f"  Melhor Fitness da Geração: {best_fitness:.2f}")
                print(f"  Melhor Fitness Global: {best_ever_fitness:.2f}")
                print(f"  Posição Final: {best_position}")
                
                if self.params.get('VERBOSE_DETAIL', False):
                    # Estatísticas da população
                    valid_paths = sum(1 for f in fitnesses if f > 0)
                    print(f"  Fitness Médio: {avg_fitness:.2f}")
                    print(f"  Caminhos Válidos: {valid_paths}/{len(fitnesses)}")
                    print(f"  Tamanho do Caminho: {len(best_path)} passos")
                    
                    # Análise de convergência
                    if self.params.get('ANALISE_CONVERGENCIA', False):
                        print(f"  Diversidade Genética: {diversity:.2%}")
                        
                        if len(self.best_fitness_history) >= 10:
                            stagnation = len(self.best_fitness_history) - max((i for i, f in enumerate(self.best_fitness_history) if f != best_ever_fitness), default=0) - 1
                            print(f"  Gerações Estagnadas: {stagnation}")
                            
                            if diversity < 0.1:
                                print(f"  ALERTA: Baixa diversidade - risco de convergência prematura!")
                            
                            if self.detect_convergence(self.best_fitness_history):
                                print(f"  ALERTA: Convergência detectada!")
                    
                    # Mostrar início do caminho
                    if len(best_path) > 1:
                        path_preview = " → ".join([f"{p}" for p in best_path[:min(5, len(best_path))]])
                        if len(best_path) > 5:
                            path_preview += " → ..."
                        print(f"  Caminho: {path_preview}")
                
                print(f"{'─'*60}")
                
                # Modo lento: adicionar delay entre gerações
                if self.params.get('MODO_LENTO', False):
                    delay = self.params.get('DELAY_GERACAO', 0.5)
                    time.sleep(delay)
                
                # Pausa interativa: esperar Enter do usuário
                pausar_a_cada = self.params.get('PAUSAR_A_CADA', 0)
                if pausar_a_cada > 0 and generation > 0 and generation % pausar_a_cada == 0:
                    input(f"\n[PAUSA] Pressione Enter para continuar (próximas {pausar_a_cada} gerações)...")
            
            # Criar nova população
            new_population = []
            
            # Elitismo: manter o melhor (se existir)
            if best_ever_chromosome is not None:
                new_population.append(copy.deepcopy(best_ever_chromosome))
            else:
                new_population.append(copy.deepcopy(best_chromosome))
            
            # Gerar o resto da população
            while len(new_population) < self.params['TAMANHO_POPULACAO']:
                # Seleção
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)
                
                # Crossover
                child1, child2 = self.crossover(parent1, parent2)
                
                # Mutação
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                new_population.append(child1)
                if len(new_population) < self.params['TAMANHO_POPULACAO']:
                    new_population.append(child2)
            
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
            'diversity_history': self.diversity_history
        }


def run_genetic(maze, params=None):
    """
    Função de conveniência para executar o GA.
    
    Args:
        maze: objeto Maze
        params: dicionário com parâmetros opcionais
        
    Returns:
        dict: resultados do GA
    """
    ga = GeneticAlgorithm(maze, params)
    return ga.run()