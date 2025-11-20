def visualize_maze_with_path(maze, path, title="LABIRINTO"):

    visual_grid = []
    for linha in maze.grid:
        visual_grid.append(list(linha))
    
    # Converter path em set para busca rápida
    path_set = set(path) if path else set()
    
    # Marcar o caminho na grade
    for i, pos in enumerate(path):
        linha, coluna = pos
        cell = maze.grid[linha][coluna]
        
        # Não sobrescrever E e S
        if cell == 'E':
            visual_grid[linha][coluna] = 'E'
        elif cell == 'S':
            visual_grid[linha][coluna] = 'S'
        else:
            # Marcar o caminho com '·' (ponto médio)
            visual_grid[linha][coluna] = '·'
    
    # Construir string de visualização
    result = []
    result.append("=" * (maze.n * 2 + 2))
    result.append(f" {title}")
    result.append("=" * (maze.n * 2 + 2))
    
    # Cabeçalho com números de coluna
    header = "  "
    for col in range(maze.n):
        header += f"{col % 10} "
    result.append(header)
    result.append("  " + "-" * (maze.n * 2))
    
    # Linhas do labirinto
    for i, linha in enumerate(visual_grid):
        row_str = f"{i % 10}|"
        for cell in linha:
            if cell == '1':
                row_str += "█ "  # Parede
            elif cell == '0':
                row_str += "  "  # Espaço livre
            elif cell == 'E':
                row_str += "E "  # Entrada
            elif cell == 'S':
                row_str += "S "  # Saída
            elif cell == '·':
                row_str += "· "  # Caminho
            else:
                row_str += "? "
        row_str += f"|{i % 10}"
        result.append(row_str)
    
    # Rodapé
    result.append("  " + "-" * (maze.n * 2))
    result.append(header)
    result.append("=" * (maze.n * 2 + 2))
    
    return "\n".join(result)


def visualize_comparison(maze, ga_path, astar_path):

    result = []
    
    # Visualização do caminho GA
    ga_visual = visualize_maze_with_path(maze, ga_path, "CAMINHO DO ALGORITMO GENÉTICO")
    
    # Visualização do caminho A*
    astar_visual = visualize_maze_with_path(maze, astar_path, "CAMINHO ÓTIMO (A*)")
    
    result.append("\n" + "=" * 80)
    result.append("VISUALIZAÇÃO DOS CAMINHOS ENCONTRADOS")
    result.append("=" * 80)
    result.append("\nLEGENDA:")
    result.append("  █ = Parede (bloqueado)")
    result.append("    = Espaço livre (pode passar)")
    result.append("  E = Entrada (ponto de partida)")
    result.append("  S = Saída (objetivo)")
    result.append("  · = Caminho percorrido")
    result.append("=" * 80)
    result.append("")
    
    # Adicionar visualização do GA
    result.append(ga_visual)
    result.append("")
    result.append(f"Estatísticas do GA:")
    result.append(f"  - Passos: {len(ga_path)}")
    result.append(f"  - Células únicas visitadas: {len(set(ga_path))}")
    
    result.append("\n")
    
    # Adicionar visualização do A*
    result.append(astar_visual)
    result.append("")
    result.append(f"Estatísticas do A*:")
    result.append(f"  - Passos: {len(astar_path)}")
    result.append(f"  - Células únicas visitadas: {len(set(astar_path))}")
    
    # Comparação
    result.append("\n" + "=" * 80)
    result.append("ANÁLISE COMPARATIVA")
    result.append("=" * 80)
    
    difference = len(ga_path) - len(astar_path)
    improvement = (difference / len(ga_path)) * 100 if len(ga_path) > 0 else 0
    
    result.append(f"Diferença de passos: {difference}")
    result.append(f"Eficiência do A*: {improvement:.2f}% mais eficiente")
    
    # Células em comum e diferentes
    ga_set = set(ga_path)
    astar_set = set(astar_path)
    common = ga_set & astar_set
    ga_only = ga_set - astar_set
    astar_only = astar_set - ga_set
    
    result.append(f"\nCélulas em comum: {len(common)}")
    result.append(f"Células apenas no GA: {len(ga_only)}")
    result.append(f"Células apenas no A*: {len(astar_only)}")
    
    result.append("=" * 80)
    result.append("")
    
    return "\n".join(result)


def create_visual_output(maze, ga_path, astar_path):
   
    return visualize_comparison(maze, ga_path, astar_path)
