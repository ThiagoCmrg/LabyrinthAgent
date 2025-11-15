"""cli.py
Breve: Interface de linha de comando para executar a simulação (recebe arquivo e modo).
Segunda linha: parse args e chama simulator; implementar depois.
"""

import sys
import os
from simulator import run_simulation


def main():
    """
    Ponto de entrada da aplicação via linha de comando.
    
    Uso:
        python solver.py <arquivo_labirinto.txt> [modo] [--pause N] [--delay S]
        
    Args:
        arquivo_labirinto.txt: caminho para o arquivo do labirinto (obrigatório)
        modo: 'fast', 'slow' ou 'ultra' (opcional, padrão: 'fast')
        --pause N: pausar a cada N gerações esperando Enter
        --delay S: adicionar S segundos de delay entre gerações
    
    Exemplos:
        python solver.py data/caso_teste_01.txt
        python solver.py data/caso_teste_01.txt slow
        python solver.py data/caso_teste_01.txt ultra --pause 10
        python solver.py data/caso_teste_01.txt slow --delay 0.5
    """
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("ERRO: Arquivo de labirinto não fornecido!")
        print("\nUso:")
        print("  python solver.py <arquivo_labirinto.txt> [modo] [--pause N] [--delay S]")
        print("\nExemplo:")
        print("  python solver.py data/caso_teste_01.txt")
        print("  python solver.py data/caso_teste_01.txt slow")
        print("  python solver.py data/caso_teste_01.txt ultra --pause 10")
        print("  python solver.py data/caso_teste_01.txt slow --delay 0.5")
        print("\nModos disponíveis:")
        print("  fast  - Exibe progresso a cada 10 gerações (padrão)")
        print("  slow  - Exibe progresso detalhado a cada geração")
        print("  ultra - Máximo detalhe + opções de pausa/delay")
        print("\nOpções extras:")
        print("  --pause N - Pausa a cada N gerações esperando Enter")
        print("  --delay S - Adiciona S segundos de delay entre gerações")
        sys.exit(1)
    
    # Obter arquivo
    maze_file = sys.argv[1]
    
    # Verificar se arquivo existe
    if not os.path.exists(maze_file):
        print(f"ERRO: Arquivo '{maze_file}' não encontrado!")
        sys.exit(1)
    
    # Obter modo (padrão: fast)
    mode = 'fast'
    pause_every = 0
    delay = 0
    
    # Processar argumentos
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg.startswith('--'):
            # Opções extras
            if arg == '--pause' and i + 1 < len(sys.argv):
                try:
                    pause_every = int(sys.argv[i + 1])
                    i += 2
                except ValueError:
                    print(f"AVISO: Valor inválido para --pause: {sys.argv[i + 1]}")
                    i += 2
            elif arg == '--delay' and i + 1 < len(sys.argv):
                try:
                    delay = float(sys.argv[i + 1])
                    i += 2
                except ValueError:
                    print(f"AVISO: Valor inválido para --delay: {sys.argv[i + 1]}")
                    i += 2
            else:
                print(f"AVISO: Opção desconhecida: {arg}")
                i += 1
        else:
            # Modo
            mode = arg.lower()
            if mode not in ['fast', 'slow', 'ultra']:
                print(f"AVISO: Modo '{mode}' não reconhecido. Usando 'fast'.")
                mode = 'fast'
            i += 1
    
    # Executar simulação
    try:
        results = run_simulation(maze_file, mode, pause_every=pause_every, delay=delay)
        
        if results is None:
            print("Simulação falhou!")
            sys.exit(1)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\nERRO durante a execução:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()