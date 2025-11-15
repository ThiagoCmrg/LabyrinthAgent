"""maze.py
Breve: Representação do labirinto (matriz n×n) e utilitários para vizinhança 8-direções.
Segunda linha: fornecer is_free() e neighbors() para uso pelo A* e simulador.
"""

class Maze:
    """
    Representa um labirinto quadrado com métodos para navegação.
    """
    
    # Direções: 8 movimentos possíveis (N, NE, E, SE, S, SW, W, NW)
    # Indexados de 0 a 7
    # Formato: (delta_linha, delta_coluna)
    DIRECTIONS = [
        (-1, 0),   # 0: Norte (cima) - diminui linha
        (-1, 1),   # 1: Nordeste (cima-direita)
        (0, 1),    # 2: Leste (direita) - aumenta coluna
        (1, 1),    # 3: Sudeste (baixo-direita)
        (1, 0),    # 4: Sul (baixo) - aumenta linha
        (1, -1),   # 5: Sudoeste (baixo-esquerda)
        (0, -1),   # 6: Oeste (esquerda) - diminui coluna
        (-1, -1),  # 7: Noroeste (cima-esquerda)
    ]
    
    DIRECTION_NAMES = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    
    def __init__(self, n, grid, pos_E, pos_S):
        """
        Inicializa o labirinto.
        
        Args:
            n: dimensão do labirinto
            grid: matriz n x n
            pos_E: posição da entrada (linha, coluna)
            pos_S: posição da saída (linha, coluna)
        """
        self.n = n
        self.grid = grid
        self.pos_E = pos_E
        self.pos_S = pos_S
    
    def is_valid(self, linha, coluna):
        """
        Verifica se uma posição está dentro dos limites do labirinto.
        """
        return 0 <= linha < self.n and 0 <= coluna < self.n
    
    def is_free(self, linha, coluna):
        """
        Verifica se uma célula é livre (não é parede).
        
        Args:
            linha, coluna: coordenadas da célula
            
        Returns:
            bool: True se a célula é livre, False caso contrário
        """
        if not self.is_valid(linha, coluna):
            return False
        
        cell = self.grid[linha][coluna]
        # Livre se for '0', 'E' ou 'S'
        return cell in ['0', 'E', 'S']
    
    def get_cell(self, linha, coluna):
        """
        Retorna o valor de uma célula.
        """
        if not self.is_valid(linha, coluna):
            return None
        return self.grid[linha][coluna]
    
    def neighbors(self, linha, coluna):
        """
        Retorna uma lista de vizinhos válidos (células livres) de uma posição.
        
        Args:
            linha, coluna: coordenadas da célula atual
            
        Returns:
            list: lista de tuplas (nova_linha, nova_coluna, custo) dos vizinhos válidos
                  custo é 1.0 para movimentos ortogonais e 1.4 para diagonais
        """
        result = []
        
        for i, (delta_linha, delta_coluna) in enumerate(self.DIRECTIONS):
            nova_linha = linha + delta_linha
            nova_coluna = coluna + delta_coluna
            
            if self.is_free(nova_linha, nova_coluna):
                # Custo: 1.0 para ortogonal, 1.4 (aproximadamente sqrt(2)) para diagonal
                cost = 1.0 if (delta_linha == 0 or delta_coluna == 0) else 1.4
                result.append((nova_linha, nova_coluna, cost))
        
        return result
    
    def move(self, linha, coluna, direction):
        """
        Move de uma posição para uma direção específica.
        
        Args:
            linha, coluna: posição atual
            direction: índice da direção (0-7)
            
        Returns:
            tuple: (nova_linha, nova_coluna) ou None se o movimento é inválido
        """
        if direction < 0 or direction >= len(self.DIRECTIONS):
            return None
        
        delta_linha, delta_coluna = self.DIRECTIONS[direction]
        nova_linha = linha + delta_linha
        nova_coluna = coluna + delta_coluna
        
        if self.is_free(nova_linha, nova_coluna):
            return (nova_linha, nova_coluna)
        
        return None