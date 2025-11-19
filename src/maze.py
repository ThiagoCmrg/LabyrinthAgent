class Maze:
    # Representação do labirinto com 8 direções
    
    DIRECTIONS = [
        (-1, 0),   # Norte
        (-1, 1),   # Nordeste
        (0, 1),    # Leste
        (1, 1),    # Sudeste
        (1, 0),    # Sul
        (1, -1),   # Sudoeste
        (0, -1),   # Oeste
        (-1, -1),  # Noroeste
    ]
    
    DIRECTION_NAMES = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    
    def __init__(self, n, grid, pos_E, pos_S):
        # Inicializa labirinto
        self.n = n
        self.grid = grid
        self.pos_E = pos_E
        self.pos_S = pos_S
    
    def is_valid(self, linha, coluna):
        # Verifica se posição está dentro dos limites
        return 0 <= linha < self.n and 0 <= coluna < self.n
    
    def is_free(self, linha, coluna):
        # Verifica se célula é livre (não parede)
        if not self.is_valid(linha, coluna):
            return False
        return self.grid[linha][coluna] in ['0', 'E', 'S']
    
    def get_cell(self, linha, coluna):
        # Retorna valor da célula
        if not self.is_valid(linha, coluna):
            return None
        return self.grid[linha][coluna]
    
    def neighbors(self, linha, coluna):
        # Retorna vizinhos válidos com custos (1.0 ortogonal, 1.4 diagonal)
        result = []
        
        for i, (delta_linha, delta_coluna) in enumerate(self.DIRECTIONS):
            nova_linha = linha + delta_linha
            nova_coluna = coluna + delta_coluna
            
            if self.is_free(nova_linha, nova_coluna):
                cost = 1.0 if (delta_linha == 0 or delta_coluna == 0) else 1.4
                result.append((nova_linha, nova_coluna, cost))
        
        return result
    
    def move(self, linha, coluna, direction):
        # Move para direção (0-7). Retorna (nova_linha, nova_coluna) ou None
        if direction < 0 or direction >= len(self.DIRECTIONS):
            return None
        
        delta_linha, delta_coluna = self.DIRECTIONS[direction]
        nova_linha = linha + delta_linha
        nova_coluna = coluna + delta_coluna
        
        if self.is_free(nova_linha, nova_coluna):
            return (nova_linha, nova_coluna)
        
        return None