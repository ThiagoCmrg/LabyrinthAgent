def parse_maze_file(filename):
    # Lê arquivo do labirinto e retorna (n, grid, pos_E, pos_S)
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Primeira linha: dimensão do labirinto
    n = int(lines[0].strip())
    
    grid = []
    pos_E = None
    pos_S = None
    
    for linha in range(n):
        line = lines[linha + 1].strip()
        row = []
        
        for coluna in range(len(line)):
            cell = line[coluna]
            
            if cell == 'E':
                pos_E = (linha, coluna)
                row.append('E')
            elif cell == 'S':
                pos_S = (linha, coluna)
                row.append('S')
            elif cell == '0':
                row.append('0')
            elif cell == '1':
                row.append('1')
            else:
                continue
        
        grid.append(row)
    
    return n, grid, pos_E, pos_S