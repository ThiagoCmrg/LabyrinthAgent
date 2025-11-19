import sys
import argparse
from simulator import run_simulation


def create_parser():
    parser = argparse.ArgumentParser(
        description='Resolução de labirinto com Algoritmo Genético + A*',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:
  python solver.py data/caso_teste_01.txt
  python solver.py data/caso_teste_01.txt slow
  python solver.py data/caso_teste_01.txt slow --population 10
  python solver.py data/caso_teste_01.txt slow --elitism --population -1
  python solver.py data/caso_teste_01.txt ultra --pause 5 --delay 0.5

Modos disponíveis:
  fast  - Rápido, mostra progresso a cada 10 gerações (padrão)
  slow  - Detalhado, mostra cada geração
  ultra - Máximo detalhe com todas as estatísticas
        '''
    )
    
    parser.add_argument('maze_file', help='Caminho para o arquivo do labirinto (.txt)')
    parser.add_argument('mode', nargs='?', default='fast', 
                       choices=['fast', 'slow', 'ultra'],
                       help='Modo de execução (padrão: fast)')
    
    parser.add_argument('--pause', type=int, default=0, metavar='N',
                       help='Pausar a cada N gerações esperando Enter')
    parser.add_argument('--delay', type=float, default=0, metavar='S',
                       help='Adicionar S segundos de delay entre gerações')
    parser.add_argument('--analyze', action='store_true',
                       help='Ativar análise de convergência/diversidade')
    parser.add_argument('--elitism', action='store_true',
                       help='Mostrar status de elitismo no CLI')
    parser.add_argument('--population', type=int, default=0, metavar='N',
                       help='Mostrar top N indivíduos por geração (use -1 para todos)')
    
    return parser


def validate_args(args):
    import os
    
    if not os.path.exists(args.maze_file):
        print(f"ERRO: Arquivo '{args.maze_file}' não encontrado!")
        return False
    
    if args.pause < 0:
        print("ERRO: --pause deve ser >= 0")
        return False
    
    if args.delay < 0:
        print("ERRO: --delay deve ser >= 0")
        return False
    
    return True


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not validate_args(args):
        sys.exit(1)
    
    try:
        results = run_simulation(
            maze_file=args.maze_file,
            mode=args.mode,
            pause_every=args.pause,
            delay=args.delay,
            analyze=args.analyze,
            show_elitism=args.elitism,
            show_population=args.population
        )
        
        if results is None:
            print("Simulação falhou!")
            sys.exit(1)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\nSimulação interrompida pelo usuário.")
        sys.exit(130)
    except Exception as e:
        print(f"\nERRO durante a execução: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
