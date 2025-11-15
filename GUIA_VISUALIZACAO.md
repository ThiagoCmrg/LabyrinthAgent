# Guia de Visualização Detalhada do Algoritmo Genético

Este guia mostra como visualizar em detalhes o funcionamento do Algoritmo Genético durante a busca pela saída do labirinto.

## Modos de Execução

### 1. **FAST** (Padrão - Rápido)
```bash
python solver.py data/caso_teste_01.txt
# ou explicitamente:
python solver.py data/caso_teste_01.txt fast
```

**O que exibe:**
- Progresso a cada 10 gerações
- Melhor fitness da geração e global
- Posição final do melhor indivíduo

**Quando usar:** Para execuções rápidas quando você só quer ver o resultado final.

---

### 2. **SLOW** (Detalhado)
```bash
python solver.py data/caso_teste_01.txt slow
```

**O que exibe:**
- Progresso de **CADA geração** (1 por 1)
- Fitness médio da população
- Número de caminhos válidos
- Preview do caminho (primeiras posições)
- Estatísticas detalhadas

**Informações mostradas:**
```
────────────────────────────────────────────────────────────
GERAÇÃO 0
────────────────────────────────────────────────────────────
  Melhor Fitness da Geração: 245.30
  Melhor Fitness Global: 245.30
  Posição Final: (3, 4)
  Fitness Médio: 145.67
  Caminhos Válidos: 87/100
  Tamanho do Caminho: 23 passos
  Caminho: (0, 0) → (1, 1) → (2, 2) → (3, 3) → (4, 4) → ...
────────────────────────────────────────────────────────────
```

**Quando usar:** Para acompanhar evolução geração por geração e entender o progresso do AG.

---

### 3. **ULTRA** (Máximo Detalhe)
```bash
python solver.py data/caso_teste_01.txt ultra
```

**O que exibe:**
- Mesmo que SLOW
- Ideal para combinar com opções --pause e --delay

**Quando usar:** Para análise profunda com pausas e delays.

---

## Opções Avançadas

### **--pause N** (Pausar a cada N gerações)
```bash
python solver.py data/caso_teste_01.txt slow --pause 10
```

**Comportamento:**
- A execução para a cada 10 gerações
- Exibe: `[PAUSA] Pressione Enter para continuar (próximas 10 gerações)...`
- Você pressiona Enter para continuar

**Quando usar:** 
- Para analisar calmamente o progresso
- Fazer anotações ou screenshots
- Aulas e demonstrações

**Exemplos:**
```bash
# Pausar a cada 5 gerações
python solver.py data/caso_teste_01.txt slow --pause 5

# Pausar a cada 20 gerações
python solver.py data/caso_teste_01.txt ultra --pause 20
```

---

### **--delay S** (Delay entre gerações)
```bash
python solver.py data/caso_teste_01.txt slow --delay 0.5
```

**Comportamento:**
- Adiciona 0.5 segundos de pausa entre cada geração
- Permite acompanhar visualmente a evolução
- Não requer interação (roda automaticamente)

**Quando usar:**
- Apresentações e demonstrações
- Gravação de vídeos
- Visualização em tempo real

**Exemplos:**
```bash
# Delay de 1 segundo (bem lento)
python solver.py data/caso_teste_01.txt slow --delay 1

# Delay de 0.2 segundos (moderado)
python solver.py data/caso_teste_01.txt slow --delay 0.2
```

---

## Combinando Opções

Você pode combinar múltiplas opções:

```bash
# Modo ultra com pausa a cada 10 gerações E delay de 0.3s
python solver.py data/caso_teste_01.txt ultra --pause 10 --delay 0.3

# Modo slow com delay de 1 segundo (para demonstrações)
python solver.py data/caso_teste_01.txt slow --delay 1

# Modo slow com pausas frequentes para análise
python solver.py data/caso_teste_01.txt slow --pause 5
```

---

## Informações Detalhadas Exibidas

### Cabeçalho Inicial
```
============================================================
INICIANDO ALGORITMO GENÉTICO
============================================================
Parâmetros:
   • Tamanho da População: 100
   • Tamanho do Cromossomo: 50 movimentos
   • Taxa de Mutação: 1.0%
   • Taxa de Crossover: 80.0%
   • Gerações Máximas: 500
   • Tamanho do Torneio: 3

Objetivo: Encontrar a saída 'S' do labirinto 10x10
   Partindo de E = (0, 0)
============================================================
```

### Por Geração (Modo SLOW/ULTRA)
- **Melhor Fitness da Geração:** Aptidão do melhor indivíduo desta geração
- **Melhor Fitness Global:** Melhor aptidão já encontrada até agora
- **Posição Final:** Onde o melhor caminho terminou
- **Fitness Médio:** Média de fitness de toda a população
- **Caminhos Válidos:** Quantos indivíduos geraram caminhos válidos
- **Tamanho do Caminho:** Número de passos do melhor caminho
- **Preview do Caminho:** Primeiras posições visitadas

### Quando Encontra a Saída
```
============================================================
SAÍDA ENCONTRADA!
============================================================
   Geração: 3
   Posição da Saída: (8, 9)
   Tamanho do Caminho: 19 passos
============================================================
```

---

## Exemplos de Uso por Cenário

### Desenvolvimento/Debug (Rápido)
```bash
python solver.py data/caso_teste_01.txt
```

### Análise Detalhada (Acompanhar Evolução)
```bash
python solver.py data/caso_teste_01.txt slow
```

### Apresentação em Aula
```bash
python solver.py data/caso_teste_01.txt slow --delay 0.5
```

### Análise Profunda (Com Pausas)
```bash
python solver.py data/caso_teste_01.txt ultra --pause 10
```

### Gravação de Vídeo
```bash
python solver.py data/caso_teste_01.txt slow --delay 1
```

### Análise Super Detalhada
```bash
python solver.py data/caso_teste_01.txt ultra --pause 5 --delay 0.3
```

---

## Entendendo os Valores

### Fitness
- **< 1000:** Caminho válido mas não encontrou S
  - Valor baseado em: exploração, proximidade à saída, movimento
- **1000000.0:** SAÍDA ENCONTRADA! 🎉

### Caminhos Válidos
- Número de indivíduos que conseguiram se mover (não ficaram presos)
- Ideal: próximo ao tamanho da população (100)

### Evolução Esperada
- Gerações iniciais: fitness baixo, muita exploração aleatória
- Gerações médias: fitness aumenta, padrões emergem
- Descoberta: fitness salta para 1000000.0

---

## Dicas de Análise

1. **Observe o Fitness Médio:** Se está aumentando, a população está evoluindo bem
2. **Caminhos Válidos:** Se muito baixo, pode indicar labirinto difícil
3. **Convergência:** Quando fitness global para de aumentar, população convergiu
4. **Preview do Caminho:** Ajuda a ver se está explorando áreas diferentes

---

## Arquivos de Saída

Independente do modo, sempre é gerado um arquivo em `outputs/` com:
- Nome: `caso_teste_XX_solucao_TIMESTAMP.txt`
- Contém: resultado completo do GA e A* para análise posterior

