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


def run_simulation(maze_file, mode='fast', verbose_interval=None, pause_every=0, delay=0, analyze=False):
    """
    Executa a simulação completa: GA + A*.
    
    Args:
        maze_file: caminho para o arquivo do labirinto
        mode: 'fast', 'slow' ou 'ultra' para controlar verbosidade
        verbose_interval: intervalo de gerações para exibir (None = automático)
        pause_every: pausar e esperar Enter a cada N gerações (0 = desabilitado)
        delay: segundos de atraso entre gerações para visualização (0 = sem delay)
        analyze: ativar análise de convergência (False = desabilitado)
        
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
        'NUM_GERACOES': 500,
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
    Gera o arquivo de saída com os resultados.
    
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
        f.write("="*60 + "\n")
        f.write("RESULTADOS DA RESOLUÇÃO DO LABIRINTO\n")
        f.write("="*60 + "\n\n")
        f.write(f"Dimensão do labirinto: {maze.n} x {maze.n}\n")
        f.write(f"Entrada (E): {maze.pos_E}\n")
        f.write(f"Saída (S): {ga_results['s_position']}\n\n")
        
        f.write("="*60 + "\n")
        f.write("FASE 1: ALGORITMO GENÉTICO\n")
        f.write("="*60 + "\n\n")
        f.write(f"[OK] Saída encontrada na geração {ga_results['generation']}\n")
        f.write(f"Posição da saída descoberta: {ga_results['s_position']}\n")
        f.write(f"Fitness final: {ga_results['fitness']:.2f}\n")
        f.write(f"Tamanho do caminho: {ga_steps} passos\n\n")
        f.write("Caminho encontrado pelo Algoritmo Genético:\n")
        f.write(ga_path_str + "\n\n")
        
        f.write("="*60 + "\n")
        f.write("FASE 2: ALGORITMO A*\n")
        f.write("="*60 + "\n\n")
        f.write("[OK] Caminho ótimo encontrado\n")
        f.write(f"Tamanho do caminho: {astar_steps} passos\n\n")
        f.write("Caminho ótimo encontrado pelo A*:\n")
        f.write(astar_path_str + "\n\n")
        
        f.write("="*60 + "\n")
        f.write("COMPARAÇÃO\n")
        f.write("="*60 + "\n\n")
        f.write(f"Passos do GA: {ga_steps}\n")
        f.write(f"Passos do A*: {astar_steps}\n")
        
        if ga_steps > astar_steps:
            f.write(f"Melhoria: {improvement:.2f}% (A* é mais eficiente)\n")
        elif ga_steps == astar_steps:
            f.write("Os caminhos têm o mesmo tamanho!\n")
        else:
            f.write("(GA encontrou um caminho mais curto - isso é raro!)\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("FIM DOS RESULTADOS\n")
        f.write("="*60 + "\n")
    
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