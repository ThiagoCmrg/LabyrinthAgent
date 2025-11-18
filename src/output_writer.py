"""output_writer.py
Responsável por escrever seções específicas do relatório de saída.
Cada função tem uma responsabilidade única (Single Responsibility Principle).
"""

from output_formatter import *


def write_header(f, maze_file, maze, ga_results):
    """Escreve cabeçalho do relatório."""
    from datetime import datetime
    
    write_section(f, "RELATÓRIO COMPLETO - RESOLUÇÃO DO LABIRINTO")
    f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    f.write(f"Arquivo: {maze_file}\n")
    f.write(f"Dimensão do labirinto: {maze.n} x {maze.n}\n")
    f.write(f"Entrada (E): {maze.pos_E}\n")
    f.write(f"Saída (S): {ga_results['s_position']}\n\n")


def write_ga_section_header(f):
    """Escreve cabeçalho da seção do AG."""
    write_section(f, "FASE 1: ALGORITMO GENÉTICO - HISTÓRICO COMPLETO")
    write_subsection(f, "PARÂMETROS DO AG:")


def write_phases_section(f, phase_logs):
    """Escreve seção de fases do AG."""
    if not phase_logs:
        return
    
    write_section(f, "FASES DO ALGORITMO GENÉTICO - CICLO COMPLETO")
    f.write("Esta seção mostra cada fase do AG na ordem em que são executadas,\n")
    f.write("permitindo entender o funcionamento interno do algoritmo.\n\n")
    
    # Agrupar por geração
    phases_by_gen = {}
    for phase in phase_logs:
        gen = phase['generation']
        if gen not in phases_by_gen:
            phases_by_gen[gen] = []
        phases_by_gen[gen].append(phase)
    
    # Escrever cada geração
    for gen in sorted(phases_by_gen.keys()):
        write_generation_header(f, gen)
        
        for phase in phases_by_gen[gen]:
            write_phase_log(f, phase)
        
        # Verificar se encontrou saída
        if _found_exit_in_generation(phases_by_gen[gen]):
            write_success_banner(f, "SAÍDA ENCONTRADA NESTA GERAÇÃO!")
            break
    
    f.write("\n")


def _found_exit_in_generation(phases):
    """Verifica se a saída foi encontrada nesta geração."""
    if not phases:
        return False
    
    last_phase = phases[-1]
    details = last_phase.get('details', {})
    return details.get('found_exit', False)


def write_ga_result(f, ga_results, ga_steps):
    """Escreve resultado final do AG."""
    f.write("\n")
    write_subsection(f, "RESULTADO FINAL:")
    f.write(f"  [OK] Saída encontrada na geração {ga_results['generation']}\n")
    f.write(f"  Posição da saída descoberta: {ga_results['s_position']}\n")
    f.write(f"  Fitness final: {ga_results['fitness']:.2f}\n")
    f.write(f"  Tamanho do caminho: {ga_steps} passos\n\n")


def write_generation_evolution(f, generation_details):
    """Escreve tabela de evolução das gerações."""
    if not generation_details:
        return
    
    write_subsection(f, "EVOLUÇÃO DAS GERAÇÕES:")
    f.write("\n")
    
    # Cabeçalho da tabela
    headers = ["Ger", "Best Gen", "Best Global", "Avg", "Min", "Max", "Div%", "Valid", "Pos Final", "Path"]
    widths = [6, 12, 12, 12, 12, 12, 8, 8, 15, 6]
    
    # Escrever cabeçalho
    for header, width in zip(headers, widths):
        f.write(f"{header:<{width}}")
    f.write("\n")
    f.write("-" * 80 + "\n")
    
    # Escrever dados
    for detail in generation_details:
        f.write(f"{detail['generation']:<6} ")
        f.write(f"{detail['best_fitness_generation']:<12.2f} ")
        f.write(f"{detail['best_fitness_global']:<12.2f} ")
        f.write(f"{detail['avg_fitness']:<12.2f} ")
        f.write(f"{detail['min_fitness']:<12.2f} ")
        f.write(f"{detail['max_fitness']:<12.2f} ")
        f.write(f"{detail['diversity']*100:<7.1f}% ")
        f.write(f"{detail['valid_paths']:<8} ")
        f.write(f"{str(detail['best_position']):<15} ")
        f.write(f"{detail['path_length']:<6}\n")
        
        # Destacar quando encontrou a solução
        if detail['best_fitness_generation'] >= 10000.0:
            f.write("-" * 80 + "\n")
            f.write(">>> SAÍDA ENCONTRADA NESTA GERAÇÃO! <<<\n")
            f.write("-" * 80 + "\n")
            break
    
    f.write("\n")


def write_ga_path(f, path):
    """Escreve caminho encontrado pelo AG."""
    write_subsection(f, "CAMINHO ENCONTRADO PELO AG:")
    f.write(format_path(path) + "\n\n")


def write_elitism_analysis(f, generation_details):
    """Escreve análise de elitismo (placeholder para expansão futura)."""
    write_subsection(f, "ANÁLISE DE ELITISMO:")
    # Análise pode ser expandida aqui se necessário


def write_astar_section(f, optimal_path):
    """Escreve seção completa do A*."""
    write_section(f, "FASE 2: ALGORITMO A* - OTIMIZAÇÃO DO CAMINHO")
    
    write_subsection(f, "CONFIGURAÇÃO:")
    write_astar_config(f)
    
    write_subsection(f, "RESULTADO:")
    f.write(f"  [OK] Caminho ótimo encontrado\n")
    f.write(f"  Tamanho do caminho: {len(optimal_path)} passos\n\n")
    
    write_subsection(f, "CAMINHO ÓTIMO ENCONTRADO PELO A*:")
    f.write(format_path(optimal_path) + "\n\n")


def write_comparison(f, ga_steps, astar_steps):
    """Escreve comparação final entre GA e A*."""
    write_section(f, "COMPARAÇÃO E ANÁLISE FINAL")
    
    difference = ga_steps - astar_steps
    improvement = ((ga_steps - astar_steps) / ga_steps) * 100 if ga_steps > 0 else 0
    
    write_subsection(f, "MÉTRICAS:")
    f.write(f"  Passos do GA: {ga_steps}\n")
    f.write(f"  Passos do A*: {astar_steps}\n")
    f.write(f"  Diferença: {difference} passos\n")
    f.write(f"  Melhoria: {improvement:.2f}% (A* é mais eficiente)\n\n")
    
    write_subsection(f, "CONCLUSÃO:")
    f.write(f"  O Algoritmo Genético descobriu a saída com sucesso, mas o caminho\n")
    f.write(f"  não era ótimo. O A* otimizou o trajeto, reduzindo em {improvement:.1f}% o número\n")
    f.write(f"  de passos necessários.\n\n")


def write_footer(f):
    """Escreve rodapé do relatório."""
    write_section(f, "FIM DO RELATÓRIO")

