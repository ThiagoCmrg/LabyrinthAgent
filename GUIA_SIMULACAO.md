# Guia: Simulação e Avaliação de Fitness

## Visão Geral

Este guia explica detalhadamente como funciona a **simulação de cromossomos no labirinto** e o **cálculo da função de aptidão (fitness)**. Esta é a peça mais crítica do Algoritmo Genético, pois determina quais soluções são boas ou ruins.

---

## O Que é Simulação?

### Conceito

**Simulação** é o processo de "executar" um cromossomo no labirinto para avaliar sua qualidade.

```
Cromossomo (genes) → Simulação → Fitness (qualidade)
   [2,5,1,3,...]   →  caminho  →    245.8
```

**Cada cromossomo é:**
- Uma sequência de movimentos (genes)
- Cada gene = direção (0-7)
- Comprimento: 50 genes (padrão)

**Simulação faz:**
1. Começa na entrada E
2. Executa cada movimento do cromossomo
3. Rastreia o caminho percorrido
4. Calcula fitness baseado no resultado

---

## Codificação: 8 Direções

### Mapeamento de Genes

```python
# Cada gene é um número de 0 a 7
DIRECTIONS = {
    0: (-1, 0),   # Norte (↑)
    1: (-1, 1),   # Nordeste (↗)
    2: (0, 1),    # Leste (→)
    3: (1, 1),    # Sudeste (↘)
    4: (1, 0),    # Sul (↓)
    5: (1, -1),   # Sudoeste (↙)
    6: (0, -1),   # Oeste (←)
    7: (-1, -1)   # Noroeste (↖)
}
```

### Exemplo Visual

```
Gene: 2 (Leste)
Antes:  E . . .
        
Depois:   E→. .
```

```
Gene: 1 (Nordeste)
Antes:  . . . .
        E . . .
        
Depois: . E . .
          ↖
        . . . .
```

---

## Fases da Simulação

### FASE 1: INICIALIZAÇÃO

```
[SIMULAÇÃO] INICIALIZAÇÃO
            Preparar estado inicial
            
              • Cromossomo: [2, 5, 1, 4, 3, 0, 7, ...]
              • Comprimento: 50 genes
              • Posição Inicial: (0, 0) [E]
              • Path: [(0, 0)]
              • Visited: {(0, 0)}
```

**O que acontece:**

```python
def evaluate_fitness(self, chromosome):
    # Estado inicial
    linha, coluna = self.maze.pos_E
    path = [(linha, coluna)]
    visited_cells = {(linha, coluna)}
```

**Estruturas de Dados:**

- **`path`**: Lista ordenada de todas as posições visitadas (com repetições)
  ```python
  [(0,0), (0,1), (0,2), (0,1), (0,2), (1,2)]
  ```

- **`visited_cells`**: Set de células únicas visitadas (sem repetições)
  ```python
  {(0,0), (0,1), (0,2), (1,2)}
  ```

**Por que ambos?**
- `path`: Mede distância percorrida (incentiva movimento)
- `visited_cells`: Mede exploração (incentiva diversidade)

---

### FASE 2: EXECUÇÃO DE MOVIMENTOS

```
[SIMULAÇÃO] EXECUTANDO MOVIMENTOS
            Processar cada gene do cromossomo
            
              • Gene Atual: 15/50
              • Direção: 2 (Leste →)
              • Posição Antes: (3, 4)
              • Posição Depois: (3, 5)
              • Status: Movimento válido ✓
```

**O que acontece:**

```python
for direction in chromosome:
    # Tentar mover
    result = self.maze.move(linha, coluna, direction)
    
    if result is None:
        # Movimento inválido (parede/limite)
        continue  # Pular este gene
    
    # Atualizar posição
    linha, coluna = result
    path.append((linha, coluna))
    visited_cells.add((linha, coluna))
```

**Exemplo Passo a Passo:**

```
Cromossomo: [2, 2, 1, 5, 4]
Labirinto:
  E . . #
  . # . .
  . . . S

Passo 0: Início em E (0,0)
Passo 1: Gene=2 (→) → (0,1) ✓
Passo 2: Gene=2 (→) → (0,2) ✓
Passo 3: Gene=1 (↗) → parede # ✗ (ignorado)
Passo 4: Gene=5 (↙) → (1,1) ✗ (parede) (ignorado)
Passo 5: Gene=4 (↓) → (1,2) ✓

path = [(0,0), (0,1), (0,2), (1,2)]
visited_cells = {(0,0), (0,1), (0,2), (1,2)}
```

---

### FASE 3: TRATAMENTO DE MOVIMENTOS INVÁLIDOS

```
[SIMULAÇÃO] MOVIMENTO INVÁLIDO
            Tentativa de movimento para parede/limite
            
              • Gene: 23
              • Direção: 0 (Norte ↑)
              • Posição Atual: (0, 5)
              • Tentativa: (-1, 5) ← FORA DO LIMITE
              • Ação: Ignorar e continuar
```

**Estratégia: Skip (Pular)**

```python
result = self.maze.move(linha, coluna, direction)

if result is None:
    # NÃO retornar imediatamente!
    # NÃO penalizar drasticamente!
    # Simplesmente pular e tentar próximo gene
    continue
```

**Por que pular em vez de penalizar?**

❌ **Estratégia Ruim:** Penalizar ou parar
```python
if result is None:
    return 0.0, (linha, coluna), path  # Fitness zero - muito severo!
```

**Problemas:**
- Converge muito lentamente
- Pune exploração excessivamente
- Cromossomos ficam "com medo" de tentar

✅ **Nossa Estratégia:** Ignorar gracefully
```python
if result is None:
    continue  # Tenta próximo movimento
```

**Vantagens:**
- ✅ Permite cromossomos robustos
- ✅ Movimento inválido não destrói toda tentativa
- ✅ Incentiva experimentação
- ✅ Converge mais rápido

---

### FASE 4: VERIFICAÇÃO DE SUCESSO

```
[SIMULAÇÃO] VERIFICAÇÃO DE SUCESSO
            Checando se encontrou a saída
            
              • Posição Atual: (8, 9)
              • Célula: S ← SAÍDA ENCONTRADA! 🎉
              • Comprimento do Caminho: 15
              • Fitness: 10066.67
```

**O que acontece:**

```python
# A cada movimento bem-sucedido
if self.maze.get_cell(linha, coluna) == 'S':
    # SOLUÇÃO ENCONTRADA!
    BASE_SUCCESS = 10000.0
    efficiency_bonus = 1000.0 / len(path)
    
    return BASE_SUCCESS + efficiency_bonus, (linha, coluna), path
```

**Fitness Híbrido:**

```
Fitness = BASE_SUCCESS + EFFICIENCY_BONUS
        = 10000.0 + (1000.0 / comprimento_caminho)
```

**Exemplos:**

| Comprimento | Cálculo | Fitness Final | Qualidade |
|-------------|---------|---------------|-----------|
| 10 passos | 10000 + 1000/10 | **10100.00** | Excelente |
| 20 passos | 10000 + 1000/20 | **10050.00** | Bom |
| 50 passos | 10000 + 1000/50 | **10020.00** | Aceitável |
| 100 passos | 10000 + 1000/100 | **10010.00** | Ineficiente |

**Por que Fitness Híbrido?**

✅ **Vantagens:**
1. Todos os sucessos têm fitness > 10000 (dominam não-sucessos)
2. Diferencia qualidade entre sucessos
3. AG pode otimizar **após** encontrar saída
4. Elitismo preserva melhor solução automaticamente

❌ **Alternativa Ruim:** Fitness fixo
```python
if encontrou_S:
    return 1000000.0  # Todos os sucessos iguais
```
- Não diferencia caminho de 10 vs 100 passos
- AG não evolui após primeiro sucesso

---

### FASE 5: CÁLCULO DE FITNESS HEURÍSTICO (Caso não encontre S)

```
[SIMULAÇÃO] FITNESS HEURÍSTICO
            Caminho não encontrou S - avaliar progresso
            
              • Posição Final: (6, 8)
              • Posição da Saída: (8, 9)
              • Distância até S: 3
              • Células Visitadas: 18
              • Comprimento do Caminho: 25
              • Fitness: 142.5
```

**O que acontece:**

```python
# Se todos os 50 genes foram executados e não achou S:

# 1. Calcular distância até a saída (Manhattan)
linha_saida, coluna_saida = self.maze.pos_S
distance_to_exit = abs(linha - linha_saida) + abs(coluna - coluna_saida)

# 2. Bônus por exploração
exploration_bonus = len(visited_cells) * 10.0

# 3. Penalidade por distância
distance_penalty = distance_to_exit * 5.0

# 4. Bônus por movimento
movement_bonus = len(path) * 0.5

# 5. Combinar componentes
fitness = exploration_bonus + movement_bonus - distance_penalty
fitness = max(0.1, fitness)  # Mínimo 0.1

return fitness, (linha, coluna), path
```

---

## Componentes da Função de Aptidão

### 1. Bônus de Exploração (Principal)

```python
exploration_bonus = len(visited_cells) * 10.0
```

**Objetivo:** Incentivar descoberta de novas áreas

**Exemplo:**
```
Cromossomo A visita: {(0,0), (0,1), (0,2)} → 3 células
Bônus A = 3 × 10.0 = 30.0

Cromossomo B visita: {(0,0), (0,1), (1,1), (2,1), (2,2)} → 5 células
Bônus B = 5 × 10.0 = 50.0

B é melhor! ✓
```

**Por que peso 10.0?**
- Componente mais importante (antes de encontrar S)
- Favorece cromossomos exploradores
- Balanceado com penalidade de distância (peso 5.0)

---

### 2. Penalidade de Distância

```python
distance_penalty = distance_to_exit * 5.0
```

**Objetivo:** Guiar em direção à saída

**Exemplo:**
```
Cromossomo A termina em (2, 3), S está em (8, 9)
Distância = |8-2| + |9-3| = 6 + 6 = 12
Penalidade = 12 × 5.0 = 60.0

Cromossomo B termina em (7, 8), S está em (8, 9)
Distância = |8-7| + |9-8| = 1 + 1 = 2
Penalidade = 2 × 5.0 = 10.0

B tem menor penalidade! ✓
```

**⚠️ Observação Importante:**

Esta componente usa `pos_S` (posição da saída), que o AG **não deveria** conhecer!

**Justificativa:**
- Em ambiente acadêmico/teste: Acelera convergência
- Em cenário 100% realista: Remover ou substituir por métrica cega

**Alternativa Realista:**
```python
# Distância da entrada (não usa pos_S)
distance_from_start = abs(linha - linha_entrada) + abs(coluna - coluna_entrada)
exploration_bonus = distance_from_start * 2.0  # Incentiva se afastar de E
```

---

### 3. Bônus de Movimento

```python
movement_bonus = len(path) * 0.5
```

**Objetivo:** Incentivar ação (não ficar parado)

**Exemplo:**
```
Cromossomo A: [0, 0, 0, ...]  → bate em parede, path = [(0,0)]
Bônus A = 1 × 0.5 = 0.5

Cromossomo B: [2, 2, 2, ...]  → move 10 vezes, path = [(0,0), (0,1), ..., (0,10)]
Bônus B = 11 × 0.5 = 5.5

B é mais ativo! ✓
```

**Por que peso baixo (0.5)?**
- Componente secundária
- Evita que cromossomos "andem em círculos" só para ganhar pontos
- Balanceado com exploração (10.0) e distância (5.0)

---

### 4. Fitness Mínimo

```python
fitness = max(0.1, fitness)
```

**Objetivo:** Evitar fitness zero ou negativo

**Por que isso importa?**

❌ **Sem mínimo:**
```python
exploration = 2 × 10.0 = 20.0
distance_penalty = 8 × 5.0 = 40.0
movement = 3 × 0.5 = 1.5

fitness = 20.0 + 1.5 - 40.0 = -18.5  ← NEGATIVO!
```

✅ **Com mínimo:**
```python
fitness = max(0.1, -18.5) = 0.1  ← Sempre positivo
```

**Vantagens:**
- Evita divisões por zero em seleção por roleta
- Garante todos os cromossomos têm algum valor
- Boa prática de AG

---

## Fórmula Completa do Fitness

### Caso 1: Saída Encontrada (S alcançado)

```
FITNESS = 10000.0 + (1000.0 / comprimento_caminho)

Faixa: [10010, 10100+]
```

**Características:**
- ✅ Sempre > 10000 (supera qualquer fitness heurístico)
- ✅ Diferencia qualidade (caminhos curtos têm fitness maior)
- ✅ Garante elitismo funciona

---

### Caso 2: Saída NÃO Encontrada (fitness heurístico)

```
FITNESS = max(0.1, (visited_cells × 10.0) + (path_length × 0.5) - (distance_to_S × 5.0))

Faixa típica: [0.1, 500]
```

**Balanceamento dos Pesos:**

```
Componente          | Peso | Típico | Máximo (labirinto 10×10)
--------------------+------+--------+--------------------------
exploration_bonus   | 10.0 |  80    | ~1000 (visitar tudo)
movement_bonus      |  0.5 |  12.5  | ~25 (50 movimentos)
distance_penalty    | -5.0 | -50    | -100 (canto oposto)
--------------------+------+--------+--------------------------
FITNESS típico      |      | 42.5   | ~925
```

**Exemplos Reais:**

```python
# Cromossomo A: Explorador preguiçoso
visited = 8, path = 10, distance = 14
fitness = (8×10) + (10×0.5) - (14×5) = 80 + 5 - 70 = 15.0

# Cromossomo B: Ativo mas longe
visited = 15, path = 25, distance = 12
fitness = (15×10) + (25×0.5) - (12×5) = 150 + 12.5 - 60 = 102.5

# Cromossomo C: Explorador focado
visited = 20, path = 30, distance = 3
fitness = (20×10) + (30×0.5) - (3×5) = 200 + 15 - 15 = 200.0

Ranking: C > B > A  ✓
```

---

## Comparação de Funções de Aptidão

### ❌ Função Simplista (Apenas Distância)

```python
fitness = -distance_to_exit
```

**Problemas:**
- Não incentiva exploração
- Converge para caminhos diretos bloqueados
- Fica preso em mínimos locais

---

### ❌ Função Apenas Exploração

```python
fitness = len(visited_cells)
```

**Problemas:**
- Não guia em direção a objetivo
- Favorece caminhos aleatórios longos
- Nunca converge

---

### ✅ Nossa Função (Multi-Objetivo)

```python
fitness = exploration + movement - distance
```

**Vantagens:**
- ✅ Explora novas áreas
- ✅ Move-se ativamente
- ✅ Guia em direção geral (com distance)
- ✅ Balanceamento entre exploração e convergência

---

## Estatísticas Típicas de Simulação

### Geração 0 (Aleatória)

```
População: 100 cromossomos
Simulações: 100

Melhor Fitness: 287.45  (não achou S)
Fitness Médio: 124.32
Pior Fitness: 34.12
Caminhos Válidos: 97/100
```

**Interpretação:**
- Nenhum achou S (todos < 10000)
- Melhor explorou ~28 células
- 3 cromossomos quase não se moveram

---

### Geração 1 (Após Crossover + Mutação)

```
Simulações: 100

Melhor Fitness: 10067.23  🎉 (ACHOU S!)
Fitness Médio: 245.67
Pior Fitness: 45.12
```

**Interpretação:**
- ✓ Um cromossomo encontrou a saída!
- Fitness 10067.23 = caminho com ~15 passos
- Fitness médio dobrou (população melhorou)

---

## Visualização da Simulação

### Exemplo de Caminho

```
Cromossomo: [2, 2, 1, 1, 4, 3, 2, ...]

Labirinto 5×5:
  E . . # .
  . # . . .
  . . . # .
  # . . . .
  . . . . S

Simulação:
  Passo 0: E (0,0)
  Passo 1: gene=2 (→) → (0,1) ✓
  Passo 2: gene=2 (→) → (0,2) ✓
  Passo 3: gene=1 (↗) → parede # (ignorado)
  Passo 4: gene=1 (↗) → parede # (ignorado)
  Passo 5: gene=4 (↓) → (1,2) ✓
  Passo 6: gene=3 (↘) → (2,3) ✓
  Passo 7: gene=2 (→) → parede # (ignorado)
  ...

Path: [(0,0), (0,1), (0,2), (1,2), (2,3), ...]
Visited: {(0,0), (0,1), (0,2), (1,2), (2,3), ...}
Fitness: 178.5 (não achou S ainda)
```

---

## Debugging: Como Analisar Fitness

### 1. Fitness Muito Baixo (< 50)

**Possíveis Causas:**
- Cromossomo bate em paredes repetidamente
- Explora poucas células
- Fica muito longe da saída

**Solução:**
- Aumentar taxa de mutação temporariamente
- Verificar se labirinto tem caminho viável

---

### 2. Fitness Não Melhora (Estagnação)

**Possíveis Causas:**
- Convergência prematura
- Diversidade baixa
- Mínimo local

**Solução:**
- Aumentar mutação
- Aumentar população
- Ajustar balanceamento dos pesos

---

### 3. Encontrou S mas Caminho Longo

**Exemplo:**
```
Fitness: 10012.5  (caminho com 80 passos)
```

**Interpretação:**
- AG achou solução (fitness > 10000) ✓
- Mas caminho é muito ineficiente
- A* vai otimizar depois

**Isso é normal!** AG é para descoberta, A* para otimização.

---

## Otimizações de Performance

### 1. Cache de Posições

❌ **Lento:**
```python
if (linha, coluna) == self.maze.pos_S:
    # Busca em objeto toda vez
```

✅ **Rápido:**
```python
if self.maze.get_cell(linha, coluna) == 'S':
    # Acesso direto à matriz
```

---

### 2. Set vs List para Visited

❌ **Lento (O(n) por busca):**
```python
if (linha, coluna) not in visited_list:
```

✅ **Rápido (O(1) por busca):**
```python
if (linha, coluna) not in visited_set:
```

---

### 3. Early Return para Sucesso

✅ **Eficiente:**
```python
if self.maze.get_cell(linha, coluna) == 'S':
    return fitness, pos, path  # Para imediatamente
```

Não processa genes restantes se já achou!

---

## Conclusão

A simulação e função de aptidão são o **coração do Algoritmo Genético**:

1. **Simulação robusta:** Ignora movimentos inválidos gracefully
2. **Fitness híbrido:** Diferencia sucessos por qualidade
3. **Multi-objetivo:** Balanceia exploração, movimento e convergência
4. **Matematicamente fundamentado:** Pesos balanceados por experimentação

**Fórmula Final:**

```
SE encontrou S:
    FITNESS = 10000 + (1000 / comprimento)
SENÃO:
    FITNESS = max(0.1, exploration×10 + movement×0.5 - distance×5)
```

Esta função guia a evolução de cromossomos aleatórios até soluções viáveis em poucas gerações! 🧬✨

