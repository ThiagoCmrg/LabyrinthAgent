"""simulator.py
Orquestra a execução do AG; detecta descoberta de S e aciona o A* para otimização.
Gera arquivos de saída em `outputs/` e controla modos fast/slow.
Refatorado com Clean Code: funções pequenas, responsabilidade única.
"""

import os
from datetime import datetime
from parser import parse_maze_file
from maze import Maze
from genetic import run_genetic
from a_star import a_star
from output_writer import *


def _determine_verbose_interval(mode, custom_interval):
    """Determina intervalo de verbosidade baseado no modo."""
    if custom_interval is not None:
        return custom_interval
    return 1 if mode in ['slow', 'ultra'] else 10


def _build_ga_params(mode, verbose_interval, pause_every, delay, analyze, show_elitism, show_population):
    """Constrói dicionário de parâmetros do AG."""
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
    """Imprime cabeçalho da simulação."""
    print(f"\n{'='*60}")
    print(f"SIMULAÇÃO DE RESOLUÇÃO DE LABIRINTO")
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
    print(f"   Saída (S): {pos_S} (posição real - não conhecida pelo AG)")
    return maze


def _run_genetic_phase(maze, ga_params):
    """Executa fase do Algoritmo Genético."""
    print("\n" + "="*60)
    print("FASE 1: DESCOBERTA DA SAÍDA COM ALGORITMO GENÉTICO")
    print("="*60)
    return run_genetic(maze, ga_params)


def _run_astar_phase(maze, s_position):
    """Executa fase do A*."""
    print("\n" + "="*60)
    print("FASE 2: OTIMIZAÇÃO DO CAMINHO COM A*")
    print("="*60)
    print(f"Executando A* de {maze.pos_E} até {s_position}...")
    return a_star(maze, maze.pos_E, s_position)


def _print_summary(ga_results, optimal_path):
    """Imprime resumo final da simulação."""
    improvement = ((len(ga_results['path']) - len(optimal_path)) / len(ga_results['path'])) * 100
    
    print(f"\n{'='*60}")
    print("RESUMO FINAL")
    print(f"{'='*60}")
    print(f"   Saída encontrada na geração: {ga_results['generation']}")
    print(f"   Posição da saída: {ga_results['s_position']}")
    print(f"   Passos do caminho AG: {len(ga_results['path'])}")
    print(f"   Passos do caminho A*: {len(optimal_path)}")
    print(f"   Melhoria do A*: {improvement:.2f}%")
    print(f"{'='*60}\n")


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
    _print_summary(ga_results, optimal_path)
    
    return {
        'ga_results': ga_results,
        'optimal_path': optimal_path,
        'output_file': output_file
    }


def generate_output_file(maze_file, maze, ga_results, optimal_path):
    """
    Gera o arquivo de saída com os resultados completos.
    Refatorado com Clean Code: delega escrita para funções especializadas.
    """
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
        write_comparison(f, ga_steps, astar_steps)
        write_footer(f)
    
    return output_file

