## Requisitos

- Python 3.x
- Nenhuma dependência externa (usa apenas biblioteca padrão)

## Instalação

### 1. Clonar ou baixar o repositório

```bash
git clone https://github.com/ThiagoCmrg/LabyrinthAgent.git
```

### 2. Verificar Python instalado

```bash
python --version
```

Deve retornar Python 3.x (ex: Python 3.10)

## Como Rodar

### Execução Básica

```bash
python solver.py data/caso_teste_01.txt
```

### Modos de Execução

#### 1. Modo FAST (padrão - rápido)
Mostra progresso a cada 10 gerações:

```bash
python solver.py data/caso_teste_01.txt fast
```

#### 2. Modo SLOW (detalhado)
Mostra cada geração:

```bash
python solver.py data/caso_teste_01.txt slow
```

#### 3. Modo ULTRA (máximo detalhe)
Mostra todas as estatísticas:

```bash
python solver.py data/caso_teste_01.txt ultra
```

### Opções Adicionais

**Ver população em detalhes:**
```bash
python solver.py data/caso_teste_01.txt slow --population -1
```

**Com análise de convergência:**
```bash
python solver.py data/caso_teste_01.txt slow --analyze
```

**Com pausas entre gerações:**
```bash
python solver.py data/caso_teste_01.txt slow --pause 10
```

**Com delay entre gerações:**
```bash
python solver.py data/caso_teste_01.txt slow --delay 0.5
```

## Arquivos de Teste

Existem 2 casos de teste fornecidos em `data/`:

- `caso_teste_01.txt` - Labirinto 10x10 (recomendado para teste rápido)
- `caso_teste_02.txt` - Labirinto 10x10 alternativo

Para usar outro arquivo:
```bash
python solver.py data/seu_arquivo.txt
```

## Saída

A execução gera:
1. **Console Output**: Mostra progresso do AG e resultado final
2. **Arquivo em `outputs/`**: Relatório completo com:
   - Parâmetros do AG
   - Histórico de gerações
   - Caminho encontrado pelo AG
   - Caminho otimizado pelo A*
   - Análise comparativa


## Exemplos de Uso

### Teste Rápido (2-3 segundos)
```bash
python solver.py data/caso_teste_01.txt fast
```

### Teste com Detalhes Completos
```bash
python solver.py data/caso_teste_01.txt slow --population -1
```

### Teste com Análise Automática
```bash
python solver.py data/caso_teste_01.txt slow --analyze
```

## Algoritmos Implementados
### Algoritmo Genético (Fase 1)
- **Objetivo**: Descobrir localização da saída
- **Codificação**: Sequência de 50 movimentos (0-7 para 8 direções)
- **Heurística (Fitness)**:
  - Se encontrou a saída: `fitness = 10000 + bonus_eficiencia`
  - Se não encontrou: `fitness = células_exploradas + proximidade_saída - distância_percorrida`
  - Prioriza: descoberta da saída > exploração > proximidade > eficiência
- **Seleção**: Torneio determinístico (k=3)
- **Crossover**: Um ponto
- **Mutação**: Gene por gene (1%)

### A* (Fase 2)
- **Objetivo**: Encontrar caminho ótimo do início até saída
- **Heurística**: Octile (admissível para 8 direções)
- **Custo ortogonal**: 1.0
- **Custo diagonal**: 1.4 (≈√2)

## Tempo de Execução

| Modo | Tempo (caso_teste_01) |
|------|----------------------|
| fast | ~1-2 segundos |
| slow | ~5-10 segundos |
| ultra | ~10-20 segundos |