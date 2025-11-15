"""
solver.py
Ponto de entrada principal para o resolvedor de labirinto.

Uso:
    python solver.py <arquivo_labirinto.txt>

Exemplo:
    python solver.py data/caso_teste_01.txt
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli import main

if __name__ == "__main__":
    main()

