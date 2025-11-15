"""
Script de Teste de Overfitting e Convergência Prematura

Executa múltiplos testes para analisar o comportamento do AG.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser import parse_maze_file
from maze import Maze
from genetic import run_genetic


def test_multiple_runs(maze_file, num_runs=10, params=None):
    """
    Executa o AG múltiplas vezes no mesmo labirinto.
    
    Args:
        maze_file: arquivo do labirinto
        num_runs: número de execuções
        params: parâmetros customizados do GA
        
    Returns:
        dict: estatísticas agregadas
    """
    print(f"\n{'='*70}")
    print(f"TESTE DE CONVERGÊNCIA: {num_runs} execuções em {maze_file}")
    print(f"{'='*70}\n")
    
    # Carregar labirinto
    n, grid, pos_E, pos_S = parse_maze_file(maze_file)
    maze = Maze(n, grid, pos_E, pos_S)
    
    print(f"Labirinto: {n}x{n}")
    print(f"Entrada: {pos_E}, Saída: {pos_S}\n")
    
    # Configurar parâmetros
    default_params = {
        'VERBOSE': False,  # Silencioso para múltiplos testes
        'ANALISE_CONVERGENCIA': True,
        'NUM_GERACOES': 500,
        'TAMANHO_POPULACAO': 100,
        'TAXA_MUTACAO': 0.01,
        'TAXA_CROSSOVER': 0.8,
    }
    
    if params:
        default_params.update(params)
    
    print(f"Parâmetros:")
    print(f"  - População: {default_params['TAMANHO_POPULACAO']}")
    print(f"  - Taxa Mutação: {default_params['TAXA_MUTACAO']}")
    print(f"  - Taxa Crossover: {default_params['TAXA_CROSSOVER']}")
    print(f"  - Gerações Máx: {default_params['NUM_GERACOES']}")
    print(f"\n{'─'*70}\n")
    
    # Resultados
    success_count = 0
    generation_found = []
    final_diversity = []
    
    for run in range(num_runs):
        print(f"Execução {run + 1}/{num_runs}...", end=' ')
        
        result = run_genetic(maze, default_params)
        
        if result['success']:
            success_count += 1
            generation_found.append(result['generation'])
            final_diversity.append(result['diversity_history'][-1] if result['diversity_history'] else 0)
            print(f"✓ Encontrou em {result['generation']} gerações (div: {final_diversity[-1]:.1%})")
        else:
            print(f"✗ Não encontrou")
            final_diversity.append(result['diversity_history'][-1] if result['diversity_history'] else 0)
    
    # Estatísticas
    print(f"\n{'='*70}")
    print(f"RESULTADOS")
    print(f"{'='*70}\n")
    
    success_rate = (success_count / num_runs) * 100
    print(f"Taxa de Sucesso: {success_count}/{num_runs} ({success_rate:.1f}%)")
    
    if generation_found:
        avg_gen = sum(generation_found) / len(generation_found)
        min_gen = min(generation_found)
        max_gen = max(generation_found)
        
        # Calcular desvio padrão
        variance = sum((x - avg_gen) ** 2 for x in generation_found) / len(generation_found)
        std_dev = variance ** 0.5
        
        print(f"\nGerações até Encontrar:")
        print(f"  - Média: {avg_gen:.1f}")
        print(f"  - Mínimo: {min_gen}")
        print(f"  - Máximo: {max_gen}")
        print(f"  - Desvio Padrão: {std_dev:.1f}")
    
    if final_diversity:
        avg_div = sum(final_diversity) / len(final_diversity)
        print(f"\nDiversidade Final Média: {avg_div:.1%}")
        
        low_diversity_count = sum(1 for d in final_diversity if d < 0.3)
        if low_diversity_count > 0:
            print(f"  ⚠️  {low_diversity_count}/{num_runs} execuções terminaram com baixa diversidade (<30%)")
    
    # Diagnóstico
    print(f"\n{'─'*70}")
    print(f"DIAGNÓSTICO")
    print(f"{'─'*70}\n")
    
    if success_rate == 100 and avg_gen < 20:
        print("✓ PROBLEMA FÁCIL: AG sempre encontra muito rápido")
        print("  Sugestão: Usar labirintos maiores/mais complexos")
    elif success_rate == 100 and avg_gen < 100:
        print("✓ DIFICULDADE ADEQUADA: AG consistente e eficiente")
    elif success_rate >= 70:
        print("✓ DIFICULDADE BOA: AG geralmente encontra, mas leva tempo")
    elif success_rate >= 30:
        print("⚠️  DESAFIADOR: AG tem dificuldade moderada")
        print("  Sugestão: Ajustar parâmetros ou aumentar gerações")
    else:
        print("❌ MUITO DIFÍCIL: AG raramente encontra solução")
        print("  Problema:")
        if avg_div < 0.3:
            print("    - Convergência prematura (baixa diversidade)")
            print("  Sugestões:")
            print("    - Aumentar taxa de mutação")
            print("    - Aumentar tamanho da população")
            print("    - Reduzir pressão seletiva (torneio maior)")
        else:
            print("    - Cromossomo muito curto ou labirinto complexo demais")
            print("  Sugestões:")
            print("    - Aumentar tamanho do cromossomo")
            print("    - Aumentar número de gerações")
    
    print(f"\n{'='*70}\n")
    
    return {
        'success_rate': success_rate,
        'avg_generations': avg_gen if generation_found else None,
        'std_dev': std_dev if generation_found else None,
        'avg_diversity': avg_div if final_diversity else None
    }


def main():
    """Executar testes"""
    
    print("\n" + "="*70)
    print("ANÁLISE DE OVERFITTING E CONVERGÊNCIA PREMATURA")
    print("="*70)
    
    # Teste 1: Caso fácil (baseline)
    print("\n[TESTE 1] Caso Fácil (10x10)")
    test_multiple_runs('data/caso_teste_01.txt', num_runs=10)
    
    input("\nPressione Enter para continuar para o próximo teste...")
    
    # Teste 2: Caso médio
    print("\n[TESTE 2] Caso Médio (15x15)")
    test_multiple_runs('data/caso_teste_04_labirinto.txt', num_runs=10)
    
    input("\nPressione Enter para continuar para o próximo teste...")
    
    # Teste 3: Caso difícil
    print("\n[TESTE 3] Caso Difícil (20x20)")
    test_multiple_runs('data/caso_teste_03_dificil.txt', num_runs=10)
    
    input("\nPressione Enter para continuar para o teste final...")

    print("\n[TESTE 4] Caso Extremo (25x25)")
    test_multiple_runs('data/caso_teste_05_extremo.txt', num_runs=10)

    input("\nPressione Enter para continuar para o teste final...")
    
    # Teste 4: Parâmetros desafiadores (convergência prematura)
    print("\n[TESTE 5] Caso Fácil com Parâmetros Difíceis")
    print("(População pequena + Mutação baixa)")
    test_multiple_runs('data/caso_teste_01.txt', num_runs=10, params={
        'TAMANHO_POPULACAO': 30,
        'TAXA_MUTACAO': 0.002,
        'TAXA_CROSSOVER': 0.9
    })
    
    print("\n✓ Análise completa!")
    print("Verifique os resultados acima para identificar:")
    print("  - Se o problema é muito fácil")
    print("  - Se há convergência prematura")
    print("  - Se os parâmetros estão adequados")


if __name__ == '__main__':
    main()

