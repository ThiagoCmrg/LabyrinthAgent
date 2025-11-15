"""a_star.py
Breve: Implementa o algoritmo A* em grafo para encontrar caminho ótimo entre E e S.
Segunda linha: usar heurística admissível (octile/euclidiana) para movimentos em 8-direções.
"""

import math

class Node:
    """
    Representa um nó no algoritmo A*.
    """
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position  # (x, y)
        self.parent = parent      # Nó pai
        self.g = g                # Custo do início até aqui
        self.h = h                # Heurística até o objetivo
        self.f = g + h            # Custo total
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self):
        return hash(self.position)
    
    def __lt__(self, other):
        return self.f < other.f


def heuristic_octile(pos1, pos2):
    """
    Calcula a distância octile (Chebyshev + diagonal) entre duas posições.
    Esta heurística é admissível para movimento em 8 direções.
    
    Args:
        pos1: tupla (linha, coluna)
        pos2: tupla (linha, coluna)
        
    Returns:
        float: distância heurística
    """
    diff_linha = abs(pos1[0] - pos2[0])
    diff_coluna = abs(pos1[1] - pos2[1])
    
    # Distância octile: movimentos diagonais custam sqrt(2) ≈ 1.4
    # e movimentos ortogonais custam 1
    return (max(diff_linha, diff_coluna) - min(diff_linha, diff_coluna)) * 1.0 + min(diff_linha, diff_coluna) * 1.4


def reconstruct_path(node):
    """
    Reconstrói o caminho a partir de um nó até o início.
    
    Args:
        node: nó final
        
    Returns:
        list: lista de posições (linha, coluna) do início até o fim
    """
    path = []
    current = node
    
    while current is not None:
        path.append(current.position)
        current = current.parent
    
    return path[::-1]  # Reverter para obter do início ao fim


def a_star(maze, start_pos, goal_pos):
    """
    Implementa o algoritmo A* para encontrar o caminho mais curto.
    
    Args:
        maze: objeto Maze
        start_pos: posição inicial (linha, coluna)
        goal_pos: posição objetivo (linha, coluna)
        
    Returns:
        list: caminho como lista de posições [(linha, coluna), ...] ou None se não houver caminho
    """
    # Nó inicial
    start_node = Node(start_pos, None, 0, heuristic_octile(start_pos, goal_pos))
    
    # Listas aberta e fechada
    open_list = [start_node]
    closed_set = set()
    
    # Dicionário para rastrear o melhor g para cada posição
    best_g = {start_pos: 0}
    
    while open_list:
        # Ordenar por f (custo total) e pegar o melhor
        open_list.sort()
        current_node = open_list.pop(0)
        
        # Verificar se chegamos ao objetivo
        if current_node.position == goal_pos:
            return reconstruct_path(current_node)
        
        # Adicionar à lista fechada
        closed_set.add(current_node.position)
        
        # Explorar vizinhos
        linha, coluna = current_node.position
        neighbors = maze.neighbors(linha, coluna)
        
        for nova_linha, nova_coluna, move_cost in neighbors:
            neighbor_pos = (nova_linha, nova_coluna)
            
            # Ignorar se já foi visitado
            if neighbor_pos in closed_set:
                continue
            
            # Calcular novo custo g
            tentative_g = current_node.g + move_cost
            
            # Se encontramos um caminho melhor para este vizinho
            if neighbor_pos not in best_g or tentative_g < best_g[neighbor_pos]:
                best_g[neighbor_pos] = tentative_g
                
                h = heuristic_octile(neighbor_pos, goal_pos)
                neighbor_node = Node(neighbor_pos, current_node, tentative_g, h)
                
                # Remover versão antiga se existir
                open_list = [node for node in open_list if node.position != neighbor_pos]
                
                # Adicionar novo nó
                open_list.append(neighbor_node)
    
    # Nenhum caminho encontrado
    return None
