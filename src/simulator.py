"""simulator.py
Breve: Orquestra a execução do AG; detecta descoberta de S e aciona o A* para otimização.
Segunda linha: gera arquivos de saída em `outputs/` e controla modos fast/slow.
"""

import os
from datetime import datetime
from parser import parse_maze_file
from maze import Maze
from genetic import run_genetic
from a_star import a_star


def run_simulation(maze_file, mode='fast', verbose_interval=None, pause_every=0, delay=0, analyze=False, show_elitism=False, show_population=0):
    """
    Executa a simulação completa: GA + A*.
    
    Args:
        maze_file: caminho para o arquivo do labirinto
        mode: 'fast', 'slow' ou 'ultra' para controlar verbosidade
        verbose_interval: intervalo de gerações para exibir (None = automático)
        pause_every: pausar e esperar Enter a cada N gerações (0 = desabilitado)
        delay: segundos de atraso entre gerações para visualização (0 = sem delay)
        analyze: ativar análise de convergência (False = desabilitado)
        show_elitism: mostrar status de elitismo no CLI (False = desabilitado)
        show_population: quantos indivíduos mostrar por geração (0 = nenhum, -1 = todos)
        
    Returns:
        dict: resultados da simulação
    """
    print(f"\n{'='*60}")
    print(f"SIMULAÇÃO DE RESOLUÇÃO DE LABIRINTO")
    print(f"{'='*60}")
    print(f"Arquivo: {maze_file}")
    print(f"Modo: {mode.upper()}")
    print(f"{'='*60}\n")
    
    # 1. Carregar o labirinto
    print("Carregando labirinto...")
    n, grid, pos_E, pos_S = parse_maze_file(maze_file)
    maze = Maze(n, grid, pos_E, pos_S)
    print(f"Labirinto {n}x{n} carregado com sucesso!")
    print(f"   Entrada (E): {pos_E}")
    print(f"   Saída (S): {pos_S} (posição real - não conhecida pelo AG)")
    
    # 2. Configurar parâmetros do GA baseado no modo
    if verbose_interval is None:
        if mode == 'fast':
            verbose_interval = 10
        elif mode == 'slow':
            verbose_interval = 1
        elif mode == 'ultra':
            verbose_interval = 1
        else:
            verbose_interval = 10
    
    ga_params = {
        'VERBOSE': True,
        'VERBOSE_INTERVAL': verbose_interval,
        'VERBOSE_DETAIL': mode in ['slow', 'ultra'] or analyze,
        'MODO_LENTO': delay > 0,
        'DELAY_GERACAO': delay,
        'PAUSAR_A_CADA': pause_every,
        'ANALISE_CONVERGENCIA': analyze,
        'SHOW_ELITISM': show_elitism,
        'SHOW_POPULATION': show_population if show_population >= 0 else 100,  # -1 = mostrar todos (100)
        'TRACK_HISTORY': True,  # Sempre rastrear histórico para arquivo de saída
        'TRACK_FULL_POPULATION': show_population != 0,  # Rastrear população completa se solicitado
        'TRACK_PHASES': True,  # Rastrear fases detalhadas do AG para arquivo de saída
        'NUM_GERACOES': 10,  # Suficiente para matrizes 10x10
        'TAMANHO_POPULACAO': 100,
        'TAXA_MUTACAO': 0.01,
        'TAXA_CROSSOVER': 0.8,
    }
    
    # 3. Executar o Algoritmo Genético (Fase 1)
    print("\n" + "="*60)
    print("FASE 1: DESCOBERTA DA SAÍDA COM ALGORITMO GENÉTICO")
    print("="*60)
    
    ga_results = run_genetic(maze, ga_params)
    
    if not ga_results['success']:
        print("\nERRO: O Algoritmo Genético não encontrou a saída!")
        print("   Tente ajustar os parâmetros ou aumentar o número de gerações.")
        return None
    
    # 4. Executar o A* (Fase 2)
    print("\n" + "="*60)
    print("FASE 2: OTIMIZAÇÃO DO CAMINHO COM A*")
    print("="*60)
    
    s_discovered = ga_results['s_position']
    print(f"Saída descoberta em: {s_discovered}")
    print(f"Executando A* de {pos_E} até {s_discovered}...")
    
    optimal_path = a_star(maze, pos_E, s_discovered)
    
    if optimal_path is None:
        print("ERRO: A* não encontrou um caminho (isso não deveria acontecer!)")
        return None
    
    print(f"Caminho ótimo encontrado com {len(optimal_path)} passos")
    
    # 5. Gerar arquivo de saída
    output_file = generate_output_file(
        maze_file, maze, ga_results, optimal_path
    )
    
    # 6. Exibir resultados finais
    display_results(maze, ga_results, optimal_path)
    
    print(f"\nResultados salvos em: {output_file}")
    print(f"\n{'='*60}")
    print("SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"{'='*60}\n")
    
    return {
        'ga_results': ga_results,
        'optimal_path': optimal_path,
        'output_file': output_file
    }


def generate_output_file(maze_file, maze, ga_results, optimal_path):
    """
    Gera o arquivo de saída com os resultados completos e histórico detalhado.
    
    Args:
        maze_file: nome do arquivo original
        maze: objeto Maze
        ga_results: resultados do GA
        optimal_path: caminho do A*
        
    Returns:
        str: caminho do arquivo gerado
    """
    # Criar diretório outputs se não existir
    os.makedirs('outputs', exist_ok=True)
    
    # Nome do arquivo de saída baseado no arquivo de entrada
    base_name = os.path.splitext(os.path.basename(maze_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"outputs/{base_name}_solucao_{timestamp}.txt"
    
    # Formatar caminhos
    ga_path_str = format_path(ga_results['path'])
    astar_path_str = format_path(optimal_path)
    
    # Calcular melhoria
    ga_steps = len(ga_results['path'])
    astar_steps = len(optimal_path)
    improvement = ((ga_steps - astar_steps) / ga_steps) * 100 if ga_steps > 0 else 0
    
    # Escrever arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO COMPLETO - RESOLUÇÃO DO LABIRINTO\n")
        f.write("="*80 + "\n\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Arquivo: {maze_file}\n")
        f.write(f"Dimensão do labirinto: {maze.n} x {maze.n}\n")
        f.write(f"Entrada (E): {maze.pos_E}\n")
        f.write(f"Saída (S): {ga_results['s_position']}\n\n")
        
        # FASE 1: ALGORITMO GENÉTICO DETALHADO
        f.write("="*80 + "\n")
        f.write("FASE 1: ALGORITMO GENÉTICO - HISTÓRICO COMPLETO\n")
        f.write("="*80 + "\n\n")
        
        f.write("PARÂMETROS DO AG:\n")
        f.write("-" * 80 + "\n")
        f.write(f"  Tamanho da População: 100\n")
        f.write(f"  Taxa de Mutação: 1.0%\n")
        f.write(f"  Taxa de Crossover: 80.0%\n")
        f.write(f"  Tamanho do Cromossomo: {len(ga_results['chromosome'])} genes\n")
        f.write(f"  Número Máximo de Gerações: 10 (ajustado para matrizes 10x10)\n")
        f.write(f"  Tamanho do Torneio: 3\n")
        f.write(f"  Elitismo: Ativado\n\n")
        
        # FASES DETALHADAS DO ALGORITMO GENÉTICO
        if ga_results.get('phase_logs'):
            f.write("\n")
            f.write("="*80 + "\n")
            f.write("FASES DO ALGORITMO GENÉTICO - CICLO COMPLETO\n")
            f.write("="*80 + "\n")
            f.write("Esta seção mostra cada fase do AG na ordem em que são executadas,\n")
            f.write("permitindo entender o funcionamento interno do algoritmo.\n\n")
            
            # Agrupar por geração
            phases_by_gen = {}
            for phase in ga_results['phase_logs']:
                gen = phase['generation']
                if gen not in phases_by_gen:
                    phases_by_gen[gen] = []
                phases_by_gen[gen].append(phase)
            
            # Mostrar fases de cada geração
            for gen in sorted(phases_by_gen.keys()):
                f.write(f"\n{'─'*80}\n")
                f.write(f"GERAÇÃO {gen}\n")
                f.write(f"{'─'*80}\n\n")
                
                for phase in phases_by_gen[gen]:
                    f.write(f"[FASE] {phase['phase']}\n")
                    f.write(f"       {phase['description']}\n")
                    
                    if phase['details']:
                        f.write(f"\n")
                        for key, value in phase['details'].items():
                            # Formatação especial para certos campos
                            if isinstance(value, float):
                                if key in ['rate', 'mutation_rate']:
                                    f.write(f"         • {key.replace('_', ' ').title()}: {value:.1f}%\n")
                                elif key in ['avg_fitness', 'best_fitness', 'worst_fitness']:
                                    f.write(f"         • {key.replace('_', ' ').title()}: {value:.2f}\n")
                                else:
                                    f.write(f"         • {key.replace('_', ' ').title()}: {value:.4f}\n")
                            elif isinstance(value, bool):
                                f.write(f"         • {key.replace('_', ' ').title()}: {'Sim' if value else 'Não'}\n")
                            else:
                                f.write(f"         • {key.replace('_', ' ').title()}: {value}\n")
                    
                    f.write(f"\n")
                
                # Indicar se encontrou a solução nesta geração
                if phases_by_gen[gen]:
                    last_phase = phases_by_gen[gen][-1]
                    if 'found_exit' in last_phase.get('details', {}) and last_phase['details']['found_exit']:
                        f.write(f"\n{'*'*80}\n")
                        f.write(f">>> SAÍDA ENCONTRADA NESTA GERAÇÃO! <<<\n")
                        f.write(f"{'*'*80}\n")
                        break
            
            f.write(f"\n")
        
        f.write("\n")
        f.write("RESULTADO FINAL:\n")
        f.write("-" * 80 + "\n")
        f.write(f"  [OK] Saída encontrada na geração {ga_results['generation']}\n")
        f.write(f"  Posição da saída descoberta: {ga_results['s_position']}\n")
        f.write(f"  Fitness final: {ga_results['fitness']:.2f}\n")
        f.write(f"  Tamanho do caminho: {ga_steps} passos\n\n")
        
        # Histórico detalhado de gerações
        if ga_results.get('generation_details'):
            f.write("EVOLUÇÃO DAS GERAÇÕES:\n")
            f.write("-" * 80 + "\n\n")
            
            f.write(f"{'Ger':<6} {'Best Gen':<12} {'Best Global':<12} {'Avg':<12} "
                   f"{'Min':<12} {'Max':<12} {'Div%':<8} {'Valid':<8} {'Pos Final':<15} {'Path':<6}\n")
            f.write("-" * 80 + "\n")
            
            for detail in ga_results['generation_details']:
                f.write(f"{detail['generation']:<6} "
                       f"{detail['best_fitness_generation']:<12.2f} "
                       f"{detail['best_fitness_global']:<12.2f} "
                       f"{detail['avg_fitness']:<12.2f} "
                       f"{detail['min_fitness']:<12.2f} "
                       f"{detail['max_fitness']:<12.2f} "
                       f"{detail['diversity']*100:<7.1f}% "
                       f"{detail['valid_paths']:<8} "
                       f"{str(detail['best_position']):<15} "
                       f"{detail['path_length']:<6}\n")
                
                # Destacar quando encontrou a solução
                if detail['best_fitness_generation'] >= 10000.0:
                    f.write("-" * 80 + "\n")
                    f.write(">>> SAÍDA ENCONTRADA NESTA GERAÇÃO! <<<\n")
                    f.write("-" * 80 + "\n")
                    break
            
            f.write("\n")
        
        # População completa detalhada (se rastreada)
        if ga_results.get('generation_details') and any('population' in d for d in ga_results['generation_details']):
            f.write("="*80 + "\n")
            f.write("POPULAÇÃO COMPLETA - DETALHAMENTO POR GERAÇÃO\n")
            f.write("="*80 + "\n\n")
            
            for detail in ga_results['generation_details']:
                if 'population' not in detail:
                    continue
                    
                f.write(f"\n{'─'*80}\n")
                f.write(f"GERAÇÃO {detail['generation']}\n")
                f.write(f"{'─'*80}\n\n")
                
                f.write(f"Estatísticas da Geração:\n")
                f.write(f"  Melhor Fitness: {detail['best_fitness_generation']:.2f}\n")
                f.write(f"  Fitness Médio: {detail['avg_fitness']:.2f}\n")
                f.write(f"  Diversidade: {detail['diversity']*100:.1f}%\n\n")
                
                f.write(f"População Completa ({len(detail['population'])} indivíduos):\n\n")
                f.write(f"{'Rank':<6} {'ID':<5} {'Fitness':<15} {'Posição Final':<20} {'Passos':<8} {'Células Únicas':<15}\n")
                f.write("-" * 80 + "\n")
                
                # Ordenar por fitness
                sorted_pop = sorted(detail['population'], key=lambda x: x['fitness'], reverse=True)
                
                for rank, ind in enumerate(sorted_pop, 1):
                    marker = "★" if rank == 1 else " "
                    f.write(f"{marker} {rank:<4} {ind['id']:<5} {ind['fitness']:<15.2f} "
                           f"{str(ind['position']):<20} {ind['path_length']:<8} {ind['unique_cells']:<15}\n")
                
                # Se encontrou a solução nesta geração, destacar
                if detail['best_fitness_generation'] >= 10000.0:
                    f.write("\n" + "-" * 80 + "\n")
                    f.write(">>> SOLUÇÃO ENCONTRADA NESTA GERAÇÃO! <<<\n")
                    f.write("-" * 80 + "\n")
                    break
                
                f.write("\n")
            
            f.write("\n")
        
        f.write("CAMINHO ENCONTRADO PELO AG:\n")
        f.write("-" * 80 + "\n")
        f.write(ga_path_str + "\n\n")
        
        # Análise de elitismo
        f.write("ANÁLISE DE ELITISMO:\n")
        f.write("-" * 80 + "\n")
        if ga_results.get('best_fitness_history'):
            elite_preserved = 0
            new_best = 0
            for i in range(1, len(ga_results['best_fitness_history'])):
                if ga_results['best_fitness_history'][i] == ga_results['best_fitness_history'][i-1]:
                    elite_preserved += 1
                else:
                    new_best += 1
            
            total_gens = len(ga_results['best_fitness_history']) - 1
            if total_gens > 0:
                f.write(f"  Total de gerações: {total_gens}\n")
                f.write(f"  Gerações com elite preservado: {elite_preserved} ({elite_preserved/total_gens*100:.1f}%)\n")
                f.write(f"  Gerações com novo melhor: {new_best} ({new_best/total_gens*100:.1f}%)\n")
                f.write(f"  Elitismo garantiu que o melhor indivíduo sempre sobreviveu.\n\n")
        
        # FASE 2: A*
        f.write("="*80 + "\n")
        f.write("FASE 2: ALGORITMO A* - OTIMIZAÇÃO DO CAMINHO\n")
        f.write("="*80 + "\n\n")
        
        f.write("CONFIGURAÇÃO:\n")
        f.write("-" * 80 + "\n")
        f.write(f"  Heurística: Octile (admissível para 8 direções)\n")
        f.write(f"  Custo ortogonal: 1.0\n")
        f.write(f"  Custo diagonal: 1.4 (≈√2)\n")
        f.write(f"  Versão: Grafo (garante otimalidade)\n\n")
        
        f.write("RESULTADO:\n")
        f.write("-" * 80 + "\n")
        f.write(f"  [OK] Caminho ótimo encontrado\n")
        f.write(f"  Tamanho do caminho: {astar_steps} passos\n\n")
        
        f.write("CAMINHO ÓTIMO ENCONTRADO PELO A*:\n")
        f.write("-" * 80 + "\n")
        f.write(astar_path_str + "\n\n")
        
        # COMPARAÇÃO FINAL
        f.write("="*80 + "\n")
        f.write("COMPARAÇÃO E ANÁLISE FINAL\n")
        f.write("="*80 + "\n\n")
        
        f.write("MÉTRICAS:\n")
        f.write("-" * 80 + "\n")
        f.write(f"  Passos do GA: {ga_steps}\n")
        f.write(f"  Passos do A*: {astar_steps}\n")
        f.write(f"  Diferença: {ga_steps - astar_steps} passos\n")
        
        if ga_steps > astar_steps:
            f.write(f"  Melhoria: {improvement:.2f}% (A* é mais eficiente)\n\n")
            f.write("CONCLUSÃO:\n")
            f.write("-" * 80 + "\n")
            f.write(f"  O Algoritmo Genético descobriu a saída com sucesso, mas o caminho\n")
            f.write(f"  não era ótimo. O A* otimizou o trajeto, reduzindo em {improvement:.1f}% o número\n")
            f.write(f"  de passos necessários.\n")
        elif ga_steps == astar_steps:
            f.write(f"  Os caminhos têm o mesmo tamanho!\n\n")
            f.write("CONCLUSÃO:\n")
            f.write("-" * 80 + "\n")
            f.write(f"  Excelente! O Algoritmo Genético encontrou um caminho ótimo na primeira\n")
            f.write(f"  tentativa, correspondendo ao resultado do A*.\n")
        else:
            f.write(f"  GA encontrou caminho mais curto que A* (isso é muito raro!)\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("FIM DO RELATÓRIO\n")
        f.write("="*80 + "\n")
    
    return output_file


def format_path(path):
    """
    Formata um caminho como string.
    
    Args:
        path: lista de tuplas (linha, coluna)
        
    Returns:
        str: caminho formatado
    """
    return " -> ".join([f"{pos}" for pos in path])


def display_results(maze, ga_results, optimal_path):
    """
    Exibe os resultados no console.
    """
    print("\n" + "="*60)
    print("RESUMO DOS RESULTADOS")
    print("="*60)
    
    print(f"\nFASE 1 - Algoritmo Genético:")
    print(f"   - Geração de descoberta: {ga_results['generation']}")
    print(f"   - Posição da saída: {ga_results['s_position']}")
    print(f"   - Tamanho do caminho: {len(ga_results['path'])} passos")
    
    print(f"\nFASE 2 - Algoritmo A*:")
    print(f"   - Tamanho do caminho ótimo: {len(optimal_path)} passos")
    
    improvement = ((len(ga_results['path']) - len(optimal_path)) / len(ga_results['path'])) * 100
    print(f"\nMelhoria: {improvement:.2f}%")
    
    print(f"\nCaminho do GA:")
    print(f"   {format_path(ga_results['path'][:10])}{'...' if len(ga_results['path']) > 10 else ''}")
    
    print(f"\nCaminho ótimo (A*):")
    print(f"   {format_path(optimal_path)}")