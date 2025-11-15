"""cli.py
Breve: Interface de linha de comando para executar a simulação (recebe arquivo e modo).
Segunda linha: parse args e chama simulator; implementar depois.
"""

import sys
import os

# Adicionar o diretório src ao path para importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import parse_maze_file
from maze import Maze
from genetic import run_genetic
from a_star import a_star
from visual import print_maze_with_path, print_comparison, save_results_to_file


def main():
    """
    Função principal da CLI.
    """
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python cli.py <arquivo_labirinto.txt>")
        print("Exemplo: python cli.py ../data/caso_teste_01.txt")
        sys.exit(1)
    
    maze_file = sys.argv[1]
    
    # Verificar se o arquivo existe
    if not os.path.exists(maze_file):
        print(f"ERRO: Arquivo '{maze_file}' não encontrado.")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("RESOLVEDOR DE LABIRINTO - Algoritmo Genético + A*")
    print("="*70)
    
    # FASE 0: Carregar o labirinto
    print("\n[FASE 0] Carregando labirinto...")
    try:
        n, grid, pos_E, pos_S = parse_maze_file(maze_file)
        maze = Maze(n, grid, pos_E, pos_S)
        print(f"Labirinto carregado: {n}x{n}")
        print(f"  Entrada (E): {pos_E}")
        print(f"  Saída (S): {pos_S}")
    except Exception as e:
        print(f"ERRO ao carregar labirinto: {e}")
        sys.exit(1)
    
    # FASE 1: Algoritmo Genético
    print("\n" + "="*70)
    print("[FASE 1] ALGORITMO GENÉTICO - Descobrindo a saída")
    print("="*70)
    print("Iniciando busca pela saída...\n")
    
    # Parâmetros do GA (podem ser ajustados)
    ga_params = {
        'TAMANHO_POPULACAO': 100,
        'TAXA_MUTACAO': 0.01,
        'TAXA_CROSSOVER': 0.8,
        'NUM_GERACOES': 500,
        'TAMANHO_CROMOSSOMO': max(50, (n * n) // 2),
        'TORNEIO_SIZE': 3,
        'VERBOSE': True,
        'VERBOSE_INTERVAL': 5,  # Mostrar a cada 5 gerações para acompanhar melhor
        'VERBOSE_DETAIL': True,  # Mostrar detalhes extras
    }
    
    ga_result = run_genetic(maze, ga_params)
    
    if not ga_result['success']:
        print("\nERRO: O Algoritmo Genético não conseguiu encontrar a saída.")
        print("Tente ajustar os parâmetros ou aumentar o número de gerações.")
        
        # Mesmo sem sucesso, salvar o que foi encontrado
        save_results_to_file(maze, ga_result, None, "solucao.txt")
        sys.exit(1)
    
    # Mostrar caminho do GA
    print(f"\nCaminho encontrado pelo GA: {len(ga_result['path'])} passos")
    print_maze_with_path(maze, ga_result['path'], "Caminho do Algoritmo Genético")
    
    # FASE 2: Algoritmo A*
    print("\n" + "="*70)
    print("[FASE 2] ALGORITMO A* - Encontrando caminho ótimo")
    print("="*70)
    print(f"\nBuscando caminho ótimo:")
    print(f"   Origem: {pos_E}")
    print(f"   Destino: {ga_result['s_position']}")
    print(f"\nExecutando A*...\n")
    
    astar_path = a_star(maze, pos_E, ga_result['s_position'])
    
    if astar_path is None:
        print("\nERRO: O A* não conseguiu encontrar um caminho.")
        save_results_to_file(maze, ga_result, None, "solucao.txt")
        sys.exit(1)
    
    print(f"{'═'*70}")
    print(f"CAMINHO ÓTIMO ENCONTRADO!")
    print(f"{'═'*70}")
    print(f"   • Número de passos: {len(astar_path)}")
    print(f"   • Início: {astar_path[0]}")
    print(f"   • Fim: {astar_path[-1]}")
    print(f"{'═'*70}\n")
    
    print_maze_with_path(maze, astar_path, "Caminho do A* (Ótimo)")
    
    # Comparação
    print_comparison(ga_result['path'], astar_path)
    
    # Salvar resultados
    print("\n" + "="*70)
    print("Salvando resultados...")
    print("="*70)
    save_results_to_file(maze, ga_result, astar_path, "solucao.txt")
    
    print("\n" + "="*70)
    print("RESOLUÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()