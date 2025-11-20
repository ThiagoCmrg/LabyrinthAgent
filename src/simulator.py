import os
from datetime import datetime
from parser import parse_maze_file
from maze import Maze
from genetic import run_genetic
from a_star import a_star
from output_writer import *


def _determine_verbose_interval(mode, custom_interval):
    if custom_interval is not None:
        return custom_interval
    return 1 if mode in ['slow', 'ultra'] else 10


def _build_ga_params(mode, verbose_interval, pause_every, delay, analyze, show_elitism, show_population):
    return {
        'VERBOSE': True,
        'VERBOSE_INTERVAL': verbose_interval,
        'VERBOSE_DETAIL': mode in ['slow', 'ultra'] or analyze,
        'MODO_LENTO': delay > 0,
        'DELAY_GERACAO': delay,
        'PAUSAR_A_CADA': pause_every,
        'ANALISE_CONVERGENCIA': analyze,
        'SHOW_ELITISM': show_elitism,
        'SHOW_POPULATION': show_population if show_population >= 0 else 100,
        'TRACK_HISTORY': True,
        'TRACK_FULL_POPULATION': show_population != 0,
        'TRACK_PHASES': True,
        'NUM_GERACOES': 10,  # Otimizado para matrizes 10x10
        'TAMANHO_POPULACAO': 100,
        'TAXA_MUTACAO': 0.01,
        'TAXA_CROSSOVER': 0.8,
    }


def _print_simulation_header(maze_file, mode):
    print(f"\n{'=' * 60}")
    print(f"SIMULACAO DE RESOLUCAO DE LABIRINTO")
    print(f"{'='*60}")
    print(f"Arquivo: {maze_file}")
    print(f"Modo: {mode.upper()}")
    print(f"{'='*60}\n")


def _load_maze(maze_file):
    """Carrega labirinto do arquivo."""
    print("Carregando labirinto...")
    n, grid, pos_E, pos_S = parse_maze_file(maze_file)
    maze = Maze(n, grid, pos_E, pos_S)
    print(f"Labirinto {n}x{n} carregado com sucesso!")
    print(f"   Entrada (E): {pos_E}")
    print(f"   Saida (S): {pos_S} (posicao real - nao conhecida pelo AG)")
    return maze


def _run_genetic_phase(maze, ga_params):
    print("\n" + "="*60)
    print("FASE 1: DESCOBERTA DA SAIDA COM ALGORITMO GENETICO")
    print("="*60)
    return run_genetic(maze, ga_params)


def _run_astar_phase(maze, s_position):
    print("\n" + "="*60)
    print("FASE 2: OTIMIZACAO DO CAMINHO COM A*")
    print("="*60)
    print(f"Executando A* de {maze.pos_E} ate {s_position}...")
    return a_star(maze, maze.pos_E, s_position)


def _print_summary(ga_results, optimal_path, maze):
    improvement = ((len(ga_results['path']) - len(optimal_path)) / len(ga_results['path'])) * 100
    
    print(f"\n{'='*60}")
    print("RESUMO FINAL")
    print(f"{'='*60}")
    print(f"   Saida encontrada na geracao: {ga_results['generation']}")
    print(f"   Posicao da saida: {ga_results['s_position']}")
    print(f"   Passos do caminho AG: {len(ga_results['path'])}")
    print(f"   Passos do caminho A*: {len(optimal_path)}")
    print(f"   Melhoria do A*: {improvement:.2f}%")
    print(f"{'='*60}\n")
    
    # Imprimir visualização dos caminhos
    from visualizer import create_visual_output
    visual_output = create_visual_output(maze, ga_results['path'], optimal_path)
    print(visual_output)


def run_simulation(maze_file, mode='fast', verbose_interval=None, pause_every=0, delay=0, analyze=False, show_elitism=False, show_population=0):
    _print_simulation_header(maze_file, mode)
    
    # 1. Carregar o labirinto
    maze = _load_maze(maze_file)
    
    # 2. Configurar parâmetros do GA
    verbose_interval = _determine_verbose_interval(mode, verbose_interval)
    ga_params = _build_ga_params(mode, verbose_interval, pause_every, delay, 
                                   analyze, show_elitism, show_population)
    
    # 3. Executar o Algoritmo Genético
    ga_results = _run_genetic_phase(maze, ga_params)
    if not ga_results['success']:
        print("\nERRO: O Algoritmo Genético não encontrou a saída!")
        print("   Tente ajustar os parâmetros ou aumentar o número de gerações.")
        return None
    
    # 4. Executar o A*
    optimal_path = _run_astar_phase(maze, ga_results['s_position'])
    if optimal_path is None:
        print("ERRO: A* não encontrou caminho para a saída descoberta!")
        return None
    
    print(f"A* encontrou caminho ótimo com {len(optimal_path)} passos.")
    
    # 5. Gerar arquivo de saída
    output_file = generate_output_file(maze_file, maze, ga_results, optimal_path)
    print(f"\nResultados salvos em: {output_file}")
    
    # 6. Exibir resumo final
    _print_summary(ga_results, optimal_path, maze)
    
    return {
        'ga_results': ga_results,
        'optimal_path': optimal_path,
        'output_file': output_file
    }


def generate_output_file(maze_file, maze, ga_results, optimal_path):
    os.makedirs('outputs', exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(maze_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"outputs/{base_name}_solucao_{timestamp}.txt"
    
    ga_steps = len(ga_results['path'])
    astar_steps = len(optimal_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        write_header(f, maze_file, maze, ga_results)
        write_ga_section_header(f)
        write_ga_parameters(f, len(ga_results['chromosome']))
        write_phases_section(f, ga_results.get('phase_logs', []))
        write_ga_result(f, ga_results, ga_steps)
        write_generation_evolution(f, ga_results.get('generation_details', []))
        write_ga_path(f, ga_results['path'])
        write_elitism_analysis(f, ga_results.get('generation_details', []))
        write_astar_section(f, optimal_path)
        write_visual_comparison(f, maze, ga_results['path'], optimal_path)
        write_comparison(f, ga_steps, astar_steps)
        write_footer(f)
    
    return output_file

