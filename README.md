# Resolvedor de Labirinto - Algoritmo Genético + A*

Este projeto implementa um sistema inteligente para resolver labirintos em duas fases:

1. **Fase 1: Algoritmo Genético (GA)** - Descobre a posição da saída 'S' no labirinto
2. **Fase 2: Algoritmo A*** - Calcula o caminho ótimo da entrada 'E' até a saída 'S'

## Características

- **Algoritmo Genético completo** com:
  - Seleção por torneio
  - Crossover de um ponto
  - Mutação adaptativa
  - Elitismo
  - Função de fitness baseada em exploração

- **Algoritmo A*** otimizado com:
  - Heurística Octile (ideal para 8 direções)
  - Movimentos em 8 direções (N, S, L, O, NE, NO, SE, SO)
  - Custos diferenciados (1.0 ortogonal, 1.4 diagonal)

- **Visualização clara**:
  - Impressão do labirinto com caminhos marcados
  - Relatório detalhado no console
  - Arquivo de saída com resultados completos

## Requisitos

- Python 3.x
- Apenas bibliotecas padrão do Python (sem dependências externas)

## Uso

```bash
python solver.py <arquivo_labirinto.txt>
```

### Exemplos:

```bash
python solver.py data/caso_teste_01.txt
python solver.py data/caso_teste_02.txt
```

## Formato do Arquivo de Entrada

O arquivo de entrada deve ser um `.txt` com o seguinte formato:

```
<dimensão>
<linha1>
<linha2>
...
<linhaN>
```

Onde:
- `E` = Entrada (sempre na posição (0, 0) que é linha 0, coluna 0)
- `S` = Saída (posição desconhecida)
- `0` = Caminho livre
- `1` = Parede

**Nota sobre coordenadas**: O sistema usa a convenção **(linha, coluna)**, onde:
- Primeiro valor = número da linha (0 = primeira linha)
- Segundo valor = número da coluna (0 = primeira coluna)

### Exemplo (labirinto 5x5):

```
5
E0100
00101
10001
01100
001S
```

## Saída

O programa gera:

1. **Saída no console**:
   - Progresso do Algoritmo Genético por geração
   - Visualização do caminho encontrado pelo GA
   - Visualização do caminho ótimo do A*
   - Comparação entre os dois caminhos

2. **Arquivo `solucao.txt`**:
   - Informações do labirinto
   - Resultado completo do GA
   - Resultado completo do A*
   - Comparação e estatísticas

## Estrutura do Projeto

```
LabyrinthAgent/
├── solver.py           # Ponto de entrada principal
├── src/
│   ├── parser.py       # Leitura de arquivos de labirinto
│   ├── maze.py          # Classe Maze e utilitários
│   ├── genetic.py      # Algoritmo Genético
│   ├── a_star.py       # Algoritmo A*
│   ├── visual.py       # Visualização e formatação
│   └── cli.py          # Interface de linha de comando
├── data/
│   ├── caso_teste_01.txt
│   └── caso_teste_02.txt
└── README.md
```

## Parâmetros do Algoritmo Genético

Os parâmetros podem ser ajustados em `src/cli.py`:

```python
ga_params = {
    'TAMANHO_POPULACAO': 100,      # Tamanho da população
    'TAXA_MUTACAO': 0.01,           # Taxa de mutação (1%)
    'TAXA_CROSSOVER': 0.8,          # Taxa de crossover (80%)
    'NUM_GERACOES': 500,            # Número máximo de gerações
    'TAMANHO_CROMOSSOMO': ...,      # Tamanho do cromossomo
    'TORNEIO_SIZE': 3,              # Tamanho do torneio
    'VERBOSE': True,                # Mostrar progresso
    'VERBOSE_INTERVAL': 10,         # Intervalo de impressão
}
```

## Como Funciona

### Fase 1: Algoritmo Genético

O GA **não conhece** a posição de 'S'. Ele evolui uma população de caminhos (cromossomos) até que um deles "tropeçe" na saída.

**Representação**:
- Cromossomo = lista de movimentos [0-7]
- 0=Norte, 1=Nordeste, 2=Leste, ..., 7=Noroeste

**Função de Fitness**:
- Se o caminho encontra 'S': fitness = 1.000.000 (solução!)
- Caso contrário: fitness = distância da entrada + células únicas visitadas
- Caminho inválido (parede): fitness = 0

**Operadores**:
- **Seleção**: Torneio (melhor de 3 aleatórios)
- **Crossover**: Um ponto (80% de chance)
- **Mutação**: Troca aleatória de genes (1% por gene)
- **Elitismo**: Melhor indivíduo sempre sobrevive

### Fase 2: Algoritmo A*

Com a posição de 'S' conhecida, o A* encontra o caminho mais curto.

**Heurística Octile**:
```
dx = |x1 - x2|
dy = |y1 - y2|
h = (max(dx, dy) - min(dx, dy)) * 1.0 + min(dx, dy) * 1.4
```

Esta heurística é **admissível** e **consistente** para movimentos em 8 direções.

## Conceitos de IA Implementados

- **Algoritmos de Busca Informada**: A* com heurística admissível
- **Algoritmos Evolutivos**: Algoritmo Genético com operadores clássicos
- **Otimização**: Função de fitness multi-objetivo
- **Exploração vs. Exploração**: Balanceamento no GA

## Exemplo de Execução

```
======================================================================
RESOLVEDOR DE LABIRINTO - Algoritmo Genético + A*
======================================================================

[FASE 0] Carregando labirinto...
Labirinto carregado: 10x10
  Entrada (E): (0, 0)
  Saída (S): (9, 8)

======================================================================
[FASE 1] ALGORITMO GENÉTICO - Descobrindo a saída
======================================================================
Iniciando busca pela saída...

Geração 0: Melhor Fitness (Exploração) = 12.50
Geração 10: Melhor Fitness (Exploração) = 18.00
Geração 20: Melhor Fitness (Exploração) = 22.50
...
SAÍDA ENCONTRADA NA GERAÇÃO 87 em (9, 8)!

Caminho encontrado pelo GA: 95 passos

======================================================================
[FASE 2] ALGORITMO A* - Encontrando caminho ótimo
======================================================================
Calculando caminho ótimo de (0, 0) até (9, 8)...

Caminho ótimo encontrado: 15 passos

Resultados salvos em 'solucao.txt'

======================================================================
RESOLUÇÃO CONCLUÍDA COM SUCESSO!
======================================================================
```

## Contribuições

Este projeto foi desenvolvido como parte de um trabalho acadêmico de Inteligência Artificial.

## Licença

Este projeto é de código aberto para fins educacionais.
