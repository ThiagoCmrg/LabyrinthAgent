# Guia de Teste de Overfitting e Convergência Prematura

## Problema Identificado

Se o AG está encontrando a solução muito rápido, pode indicar:
1. **Problema fácil demais** (labirinto com caminho muito direto)
2. **Parâmetros muito favoráveis** (população grande, cromossomo longo)
3. **Falta de desafio** (labirinto pequeno)

## Como Testar Overfitting/Convergência

### 1. Análise Básica com --analyze

```bash
python solver.py data/caso_teste_01.txt slow --analyze
```

**O que será exibido:**
- **Diversidade Genética:** 0-100% (quanto maior, melhor)
- **Gerações Estagnadas:** Quantas gerações sem melhoria
- **Alertas automáticos:**
  - "Baixa diversidade - risco de convergência prematura!"
  - "Convergência detectada!"

### 2. Interpretar Métricas

#### Diversidade Genética
```
Diversidade Genética: 85.23%  ← Saudável
Diversidade Genética: 45.12%  ← Moderada
Diversidade Genética: 8.45%   ← RISCO de convergência prematura!
```

**Valores ideais:**
- > 60%: População diversificada (saudável)
- 30-60%: Convergindo (normal se próximo da solução)
- < 30%: Convergência prematura (população uniforme)

#### Gerações Estagnadas
```
Gerações Estagnadas: 5   ← Normal
Gerações Estagnadas: 25  ← Possível convergência prematura
Gerações Estagnadas: 50+ ← População convergiu sem encontrar S
```

---

## Casos de Teste por Dificuldade

### Fácil (10x10 - Original)
```bash
python solver.py data/caso_teste_01.txt slow --analyze
python solver.py data/caso_teste_02.txt slow --analyze
```
**Esperado:** Encontra em 5-20 gerações

### Médio (15x15)
```bash
python solver.py data/caso_teste_04_labirinto.txt slow --analyze
```
**Esperado:** Encontra em 20-100 gerações

### Difícil (20x20)
```bash
python solver.py data/caso_teste_03_dificil.txt slow --analyze
```
**Esperado:** Encontra em 50-200 gerações

### Extremo (25x25 - Labirinto Espiral)
```bash
python solver.py data/caso_teste_05_extremo.txt slow --analyze
```
**Esperado:** Encontra em 100-500 gerações (ou pode não encontrar!)

---

## Ajustando Parâmetros para Aumentar Dificuldade

Edite `src/simulator.py` linha 55-67 para testar diferentes configurações:

### Configuração 1: Reduzir Ajuda (Mais Difícil)
```python
ga_params = {
    'NUM_GERACOES': 500,
    'TAMANHO_POPULACAO': 50,      # ← Reduzir de 100 para 50
    'TAXA_MUTACAO': 0.005,         # ← Reduzir de 0.01 para 0.005
    'TAXA_CROSSOVER': 0.6,         # ← Reduzir de 0.8 para 0.6
    'TAMANHO_CROMOSSOMO': maze.n * 2,  # ← Cromossomo mais curto
}
```

### Configuração 2: População Pequena (Testa Diversidade)
```python
ga_params = {
    'TAMANHO_POPULACAO': 20,       # ← Muito pequena
    'TAXA_MUTACAO': 0.01,
    'TAXA_CROSSOVER': 0.8,
}
```
**Espera-se:** Convergência prematura frequente

### Configuração 3: Baixa Mutação (Testa Convergência)
```python
ga_params = {
    'TAMANHO_POPULACAO': 100,
    'TAXA_MUTACAO': 0.001,         # ← Mutação muito baixa
    'TAXA_CROSSOVER': 0.9,         # ← Crossover muito alto
}
```
**Espera-se:** População converge rapidamente para mínimo local

### Configuração 4: Cromossomo Curto (Desafio Maior)
```python
ga_params = {
    'TAMANHO_CROMOSSOMO': 30,      # ← Muito curto para labirintos grandes
}
```
**Espera-se:** Dificuldade em labirintos grandes

---

## Sinais de Overfitting/Problema Fácil

### ✅ AG Saudável
```
GERAÇÃO 0
  Fitness Médio: 145.67
  Diversidade Genética: 88.34%

GERAÇÃO 20
  Fitness Médio: 289.45
  Diversidade Genética: 72.18%

GERAÇÃO 50
  Fitness Médio: 456.23
  Diversidade Genética: 58.92%
  
GERAÇÃO 87
  SAÍDA ENCONTRADA!
```
- Fitness aumenta gradualmente
- Diversidade diminui progressivamente
- Encontra solução após exploração

### ❌ Problema Fácil Demais
```
GERAÇÃO 0
  Fitness Médio: 145.67
  Diversidade Genética: 88.34%

GERAÇÃO 3
  SAÍDA ENCONTRADA!  ← Muito rápido!
```
- Solução encontrada em < 10 gerações
- Indica caminho muito direto

### ⚠️ Convergência Prematura
```
GERAÇÃO 0
  Diversidade Genética: 85.23%

GERAÇÃO 30
  Fitness Médio: 245.67
  Diversidade Genética: 12.45%
  ALERTA: Baixa diversidade!

GERAÇÃO 50-150
  Fitness Médio: 245.67  ← Estagnado
  Gerações Estagnadas: 120
  ALERTA: Convergência detectada!

GERAÇÃO 500
  Não encontrou solução
```
- Diversidade cai rápido
- Fitness estagna
- Nunca encontra S

---

## Experimentos Recomendados

### Experimento 1: Baseline
```bash
# Rodar casos fáceis para estabelecer baseline
python solver.py data/caso_teste_01.txt slow --analyze
python solver.py data/caso_teste_02.txt slow --analyze
```
**Anotar:** Gerações até encontrar, diversidade final

### Experimento 2: Casos Difíceis
```bash
# Testar casos progressivamente mais difíceis
python solver.py data/caso_teste_04_labirinto.txt slow --analyze
python solver.py data/caso_teste_03_dificil.txt slow --analyze
python solver.py data/caso_teste_05_extremo.txt slow --analyze
```
**Observar:** 
- Demora mais?
- Diversidade se mantém?
- Convergência prematura?

### Experimento 3: Variar Parâmetros
```python
# No simulator.py, testar:

# Teste A: População pequena
'TAMANHO_POPULACAO': 30

# Teste B: Mutação baixa  
'TAXA_MUTACAO': 0.001

# Teste C: Cromossomo curto
'TAMANHO_CROMOSSOMO': 30
```
**Rodar múltiplas vezes cada configuração** (GA é estocástico!)

### Experimento 4: Análise Estatística
Rodar o mesmo caso 10 vezes e calcular:
- Média de gerações até encontrar S
- Desvio padrão
- Taxa de sucesso (% de vezes que encontrou)

---

## Métricas Avançadas para Análise

Os históricos são salvos em `ga_results`:
- `best_fitness_history[]` - Melhor fitness por geração
- `avg_fitness_history[]` - Fitness médio por geração
- `diversity_history[]` - Diversidade por geração

Você pode plotar gráficos (com matplotlib) para análise visual.

---

## Conclusão: O AG está Overfitting?

**Não há "overfitting" tradicional em AG** (não é aprendizado de máquina).

**Mas pode haver:**
1. **Convergência Prematura:** População converge para mínimo local
2. **Problema Trivial:** Labirinto fácil demais
3. **Parâmetros Generosos:** Facilitam demais a busca

**Teste com:**
- Labirintos maiores ✓ (já criados)
- Opção `--analyze` ✓ (implementada)
- Variar parâmetros ✓ (editar simulator.py)
- Múltiplas execuções (recomendado)

---

## Comandos Rápidos

```bash
# Análise completa do caso fácil
python solver.py data/caso_teste_01.txt slow --analyze

# Análise completa do caso extremo
python solver.py data/caso_teste_05_extremo.txt slow --analyze

# Ver evolução com pausas
python solver.py data/caso_teste_03_dificil.txt slow --analyze --pause 20
```

