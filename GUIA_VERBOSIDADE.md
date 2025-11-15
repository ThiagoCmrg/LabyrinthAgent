# Guia de Verbosidade - LabyrinthAgent

Este guia explica como ajustar o nível de detalhamento da simulação.

## Níveis de Verbosidade

### Nível 1: Mínimo (Apenas Resultados)
```python
ga_params = {
    'VERBOSE': False,
}
```
- Mostra apenas os resultados finais
- Sem progresso durante a execução
- Mais rápido

### Nível 2: Resumido (Padrão Recomendado)
```python
ga_params = {
    'VERBOSE': True,
    'VERBOSE_INTERVAL': 10,  # Mostra a cada 10 gerações
    'VERBOSE_DETAIL': False,  # Sem detalhes extras
}
```
- Mostra progresso a cada 10 gerações
- Informações básicas (fitness)
- Bom balanço entre informação e velocidade

### Nível 3: Detalhado (Acompanhar Raciocínio)
```python
ga_params = {
    'VERBOSE': True,
    'VERBOSE_INTERVAL': 5,  # Mostra a cada 5 gerações
    'VERBOSE_DETAIL': True,  # Com detalhes extras
}
```
- Mostra progresso a cada 5 gerações
- Inclui estatísticas da população
- Mostra preview do caminho
- **PADRÃO ATUAL**

### Nível 4: Máximo (Debug Completo)
```python
ga_params = {
    'VERBOSE': True,
    'VERBOSE_INTERVAL': 1,  # Mostra TODAS as gerações
    'VERBOSE_DETAIL': True,  # Com detalhes extras
}
```
- Mostra TODAS as gerações
- Máximo de informação
- Mais lento, ideal para entender o algoritmo

## Como Alterar

Edite o arquivo `src/cli.py` na linha ~59:

```python
# Parâmetros do GA (podem ser ajustados)
ga_params = {
    'TAMANHO_POPULACAO': 100,
    'TAXA_MUTACAO': 0.01,
    'TAXA_CROSSOVER': 0.8,
    'NUM_GERACOES': 500,
    'TAMANHO_CROMOSSOMO': max(50, (n * n) // 2),
    'TORNEIO_SIZE': 3,
    'VERBOSE': True,
    'VERBOSE_INTERVAL': 5,  # <-- ALTERE AQUI
    'VERBOSE_DETAIL': True,  # <-- E AQUI
}
```

## O que Cada Informação Significa

### Durante a Execução:
- **Melhor Fitness da Geração**: Melhor indivíduo desta geração específica
- **Melhor Fitness Global**: Melhor encontrado até agora em todas as gerações
- **Posição Final**: Onde o melhor caminho terminou
- **Fitness Médio**: Média de fitness de toda a população
- **Caminhos Válidos**: Quantos indivíduos não bateram em paredes
- **Tamanho do Caminho**: Número de passos do melhor caminho
- **Caminho**: Preview das primeiras posições visitadas

### Valores de Fitness:
- **0.0**: Caminho inválido (bateu em parede)
- **1-50**: Explorando, mas ainda longe da saída
- **1000000.0**: SAÍDA ENCONTRADA!

## Dicas

1. Use `VERBOSE_INTERVAL: 1` para labirintos pequenos (5x5)
2. Use `VERBOSE_INTERVAL: 5-10` para labirintos médios (10x10)
3. Use `VERBOSE_INTERVAL: 20-50` para labirintos grandes (>20x20)
4. Desative `VERBOSE_DETAIL` se a saída ficar muito poluída

## Execução Rápida vs Observação

**Para executar rápido:**
```bash
# Edite cli.py e configure VERBOSE: False
python solver.py data/caso_teste_01.txt
```

**Para acompanhar o raciocínio (atual):**
```bash
# Configuração já está otimizada!
python solver.py data/caso_teste_01.txt
```

Agora você pode ver como o algoritmo genético evolui passo a passo!

