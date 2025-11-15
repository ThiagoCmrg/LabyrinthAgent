"""parser.py
Breve: Lê o arquivo do labirinto e retorna (n, grid, posE, posS).
Segunda linha: grid usa '0' para livre e '1' para parede; 'E' e 'S' são detectados.
"""

def parse_maze_file(filename):
    """
    Lê um arquivo de labirinto e retorna informações estruturadas.
    
    Args:
        filename: caminho para o arquivo .txt do labirinto
        
    Returns:
        tuple: (n, grid, pos_E, pos_S)
            n: dimensão do labirinto (n x n)
            grid: matriz n x n como lista de listas
            pos_E: tupla (x, y) da posição de entrada
            pos_S: tupla (x, y) da posição de saída
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Primeira linha: dimensão do labirinto
    n = int(lines[0].strip())
    
    # Inicializar grid e posições
    grid = []
    pos_E = None
    pos_S = None
    
    # Ler as próximas n linhas
    for linha in range(n):
        line = lines[linha + 1].strip()
        row = []
        
        for coluna in range(len(line)):
            cell = line[coluna]
            
            if cell == 'E':
                pos_E = (linha, coluna)  # (linha, coluna)
                row.append('E')
            elif cell == 'S':
                pos_S = (linha, coluna)  # (linha, coluna)
                row.append('S')
            elif cell == '0':
                row.append('0')
            elif cell == '1':
                row.append('1')
            else:
                # Ignorar caracteres inválidos (espaços, etc)
                continue
        
        grid.append(row)
    
    # Validação
    if pos_E is None:
        raise ValueError("Entrada 'E' não encontrada no labirinto")
    if pos_S is None:
        raise ValueError("Saída 'S' não encontrada no labirinto")
    
    return n, grid, pos_E, pos_S