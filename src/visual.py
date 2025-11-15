"""visual.py
Breve: Funções para marcar caminhos no grid e formatar arquivos de saída legíveis.
Segunda linha: gerar representação textual do labirinto com caminho do AG e do A*.
"""

import copy


def print_maze_with_path(maze, path, title="Labirinto"):
    """
    Imprime o labirinto com um caminho marcado.
    
    Args:
        maze: objeto Maze
        path: lista de posições [(linha, coluna), ...]
        title: título para a visualização
    """
    # Criar uma cópia do grid
    display_grid = copy.deepcopy(maze.grid)
    
    # Marcar o caminho com '*'
    path_set = set(path)
    
    for linha in range(maze.n):
        for coluna in range(maze.n):
            if (linha, coluna) in path_set:
                # Não sobrescrever E e S
                if display_grid[linha][coluna] not in ['E', 'S']:
                    display_grid[linha][coluna] = '*'
    
    # Imprimir
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    
    for row in display_grid:
        print(' '.join(row))
    
    print(f"{'='*50}\n")


def format_path_output(path):
    """
    Formata um caminho como string para saída.
    
    Args:
        path: lista de posições [(linha, coluna), ...]
        
    Returns:
        str: caminho formatado
    """
    if not path:
        return "Nenhum caminho encontrado"
    
    path_str = " -> ".join([f"({linha}, {coluna})" for linha, coluna in path])
    return path_str


def save_results_to_file(maze, ga_result, astar_path, filename="solucao.txt"):
    """
    Salva os resultados em um arquivo de texto.
    
    Args:
        maze: objeto Maze
        ga_result: resultado do algoritmo genético (dict)
        astar_path: caminho do A* (lista)
        filename: nome do arquivo de saída
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("RESULTADOS DA RESOLUÇÃO DO LABIRINTO\n")
        f.write("="*60 + "\n\n")
        
        # Informações do labirinto
        f.write(f"Dimensão do labirinto: {maze.n} x {maze.n}\n")
        f.write(f"Entrada (E): {maze.pos_E}\n")
        f.write(f"Saída (S): {maze.pos_S}\n\n")
        
        # Resultados do GA
        f.write("="*60 + "\n")
        f.write("FASE 1: ALGORITMO GENÉTICO\n")
        f.write("="*60 + "\n\n")
        
        if ga_result['success']:
            f.write(f"[OK] Saída encontrada na geração {ga_result['generation']}\n")
            f.write(f"Posição da saída descoberta: {ga_result['s_position']}\n")
            f.write(f"Fitness final: {ga_result['fitness']:.2f}\n")
            f.write(f"Tamanho do caminho: {len(ga_result['path'])} passos\n\n")
            
            f.write("Caminho encontrado pelo Algoritmo Genético:\n")
            f.write(format_path_output(ga_result['path']) + "\n\n")
        else:
            f.write("[ERRO] Algoritmo genético não encontrou a saída\n\n")
        
        # Resultados do A*
        f.write("="*60 + "\n")
        f.write("FASE 2: ALGORITMO A*\n")
        f.write("="*60 + "\n\n")
        
        if astar_path:
            f.write(f"[OK] Caminho ótimo encontrado\n")
            f.write(f"Tamanho do caminho: {len(astar_path)} passos\n\n")
            
            f.write("Caminho ótimo encontrado pelo A*:\n")
            f.write(format_path_output(astar_path) + "\n\n")
        else:
            f.write("[ERRO] A* não conseguiu encontrar um caminho\n\n")
        
        # Comparação
        if ga_result['success'] and astar_path:
            f.write("="*60 + "\n")
            f.write("COMPARAÇÃO\n")
            f.write("="*60 + "\n\n")
            
            ga_length = len(ga_result['path'])
            astar_length = len(astar_path)
            
            f.write(f"Passos do GA: {ga_length}\n")
            f.write(f"Passos do A*: {astar_length}\n")
            
            if astar_length < ga_length:
                improvement = ((ga_length - astar_length) / ga_length) * 100
                f.write(f"Melhoria: {improvement:.2f}% (A* é mais eficiente)\n")
            else:
                f.write(f"O GA encontrou um caminho comparável ou melhor!\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("FIM DOS RESULTADOS\n")
        f.write("="*60 + "\n")
    
    print(f"Resultados salvos em '{filename}'")


def print_comparison(ga_path, astar_path):
    """
    Imprime uma comparação entre os dois caminhos.
    """
    print("\n" + "="*60)
    print("COMPARAÇÃO DE RESULTADOS")
    print("="*60)
    
    if ga_path and astar_path:
        print(f"Caminho do Algoritmo Genético: {len(ga_path)} passos")
        print(f"Caminho do A*: {len(astar_path)} passos")
        
        if len(astar_path) < len(ga_path):
            improvement = ((len(ga_path) - len(astar_path)) / len(ga_path)) * 100
            print(f"[OK] A* reduziu o caminho em {improvement:.1f}%")
        elif len(astar_path) == len(ga_path):
            print(f"[OK] Ambos os algoritmos encontraram caminhos de mesmo tamanho")
        else:
            print(f"[AVISO] O GA encontrou um caminho mais curto (incomum)")
    
    print("="*60 + "\n")