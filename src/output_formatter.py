def write_section(f, title, char='=', width=80):
    f.write(char * width + "\n")
    f.write(f"{title}\n")
    f.write(char * width + "\n\n")


def write_subsection(f, title, width=80):
    f.write(f"{title}\n")
    f.write("-" * width + "\n")


def write_parameters(f, params):
    for key, value in params.items():
        f.write(f"  {key}: {value}\n")
    f.write("\n")


def format_detail_value(key, value):
    key_display = key.replace('_', ' ').title()
    
    if isinstance(value, float):
        if key in ['rate', 'mutation_rate']:
            return f"{key_display}: {value:.1f}%"
        elif key in ['avg_fitness', 'best_fitness', 'worst_fitness']:
            return f"{key_display}: {value:.2f}"
        else:
            return f"{key_display}: {value:.4f}"
    elif isinstance(value, bool):
        return f"{key_display}: {'Sim' if value else 'Não'}"
    else:
        return f"{key_display}: {value}"


def write_phase_details(f, details, indent="         - "):
    if not details:
        return
    
    f.write("\n")
    for key, value in details.items():
        formatted = format_detail_value(key, value)
        f.write(f"{indent}{formatted}\n")


def write_phase_log(f, phase):
    f.write(f"[FASE] {phase['phase']}\n")
    f.write(f"       {phase['description']}\n")
    write_phase_details(f, phase.get('details', {}))
    f.write("\n")


def write_generation_header(f, generation, width=80):
    f.write(f"\n{'-' * width}\n")
    f.write(f"GERACAO {generation}\n")
    f.write(f"{'-' * width}\n\n")


def write_table_row(f, row_data, column_formats):
    formatted_values = []
    for value, fmt in zip(row_data, column_formats):
        if isinstance(fmt, str):  # É uma especificação de formato como "<6"
            if isinstance(value, float):
                formatted_values.append(f"{value:{fmt}f}")
            else:
                formatted_values.append(f"{value:{fmt}}")
        else:  # É uma tupla (width, decimal_places) para floats
            width, decimals = fmt
            formatted_values.append(f"{value:<{width}.{decimals}f}")
    
    f.write(" ".join(formatted_values) + "\n")


def write_success_banner(f, message, width=80):
    f.write("\n" + "*" * width + "\n")
    f.write(f">>> {message} <<<\n")
    f.write("*" * width + "\n")


def format_path(path, max_per_line=8):
    if not path:
        return "(vazio)"
    
    path_str = " -> ".join([f"{pos}" for pos in path])
    return path_str


def write_ga_parameters(f, chromosome_length):
    params = {
        "Tamanho da População": 100,
        "Taxa de Mutação": "1.0%",
        "Taxa de Crossover": "80.0%",
        "Tamanho do Cromossomo": f"{chromosome_length} genes",
        "Número Máximo de Gerações": "10",
        "Tamanho do Torneio": 3,
        "Elitismo": "Ativado"
    }
    write_parameters(f, params)


def write_astar_config(f):
    config = {
        "Heurística": "Octile (admissível para 8 direções)",
        "Custo ortogonal": "1.0",
        "Custo diagonal": "1.4 (≈√2)",
        "Versão": "Grafo (garante otimalidade)"
    }
    write_parameters(f, config)

