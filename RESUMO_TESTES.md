# Resumo: Como Testar Overfitting do Algoritmo Genético

## Resposta Rápida

Se o AG está encontrando a solução muito rápido, use estas 3 abordagens:

### 1. Teste com Labirintos Mais Difíceis ✓
```bash
# Fácil (10x10) - encontra em ~5-20 gerações
python solver.py data/caso_teste_01.txt slow --analyze

# Médio (15x15) - encontra em ~20-100 gerações  
python solver.py data/caso_teste_04_labirinto.txt slow --analyze

# Difícil (20x20) - encontra em ~50-200 gerações
python solver.py data/caso_teste_03_dificil.txt slow --analyze

# Extremo (25x25) - encontra em ~100-500 gerações (ou não encontra!)
python solver.py data/caso_teste_05_extremo.txt slow --analyze
```

### 2. Ative Análise de Convergência ✓
```bash
python solver.py data/caso_teste_01.txt slow --analyze
```

**Você verá:**
```
Diversidade Genética: 78.45%       ← Quão diferentes são os indivíduos
Gerações Estagnadas: 5             ← Gerações sem melhoria
ALERTA: Baixa diversidade!         ← Convergência prematura detectada
ALERTA: Convergência detectada!    ← População uniforme
```

### 3. Execute Múltiplos Testes Automaticamente ✓
```bash
python test_overfitting.py
```

Isso vai:
- Rodar 10 vezes cada labirinto
- Calcular taxa de sucesso, média, desvio padrão
- Diagnosticar automaticamente se o problema é fácil demais

---

## Interpretação dos Resultados

### ✅ AG Saudável (Dificuldade Adequada)
```
Taxa de Sucesso: 10/10 (100%)
Gerações até Encontrar:
  - Média: 87.3
  - Desvio Padrão: 23.4
Diversidade Final Média: 58.23%

DIAGNÓSTICO: DIFICULDADE ADEQUADA
```

### ⚠️ Problema Fácil Demais
```
Taxa de Sucesso: 10/10 (100%)
Gerações até Encontrar:
  - Média: 3.2          ← Muito rápido!
  - Desvio Padrão: 1.1
  
DIAGNÓSTICO: PROBLEMA FÁCIL
Sugestão: Usar labirintos maiores/mais complexos
```

### ❌ Convergência Prematura
```
Taxa de Sucesso: 2/10 (20%)       ← Taxa baixa
Diversidade Final Média: 12.45%   ← Diversidade muito baixa!

DIAGNÓSTICO: MUITO DIFÍCIL
Problema: Convergência prematura
Sugestões:
  - Aumentar taxa de mutação
  - Aumentar tamanho da população
```

---

## Ajustar Parâmetros

Edite `src/simulator.py` linhas 55-67:

```python
ga_params = {
    # Aumentar dificuldade:
    'TAMANHO_POPULACAO': 50,        # ← Reduzir de 100
    'TAXA_MUTACAO': 0.005,          # ← Reduzir de 0.01
    'TAMANHO_CROMOSSOMO': maze.n * 2,  # ← Cromossomo mais curto
    
    # Ou aumentar facilidade (evitar convergência):
    'TAMANHO_POPULACAO': 200,       # ← Aumentar
    'TAXA_MUTACAO': 0.02,           # ← Aumentar
}
```

---

## Comandos Essenciais

```bash
# 1. Teste rápido com análise
python solver.py data/caso_teste_01.txt slow --analyze

# 2. Caso extremo
python solver.py data/caso_teste_05_extremo.txt slow --analyze

# 3. Testes automáticos completos
python test_overfitting.py

# 4. Análise com pausas para observar evolução
python solver.py data/caso_teste_03_dificil.txt slow --analyze --pause 20
```

---

## Arquivos Criados

✅ **Casos de teste novos:**
- `data/caso_teste_03_dificil.txt` (20x20)
- `data/caso_teste_04_labirinto.txt` (15x15)
- `data/caso_teste_05_extremo.txt` (25x25 espiral)

✅ **Ferramentas:**
- `test_overfitting.py` - Testes automáticos
- `GUIA_TESTE_OVERFITTING.md` - Documentação completa
- Opção `--analyze` no CLI

✅ **Métricas implementadas:**
- Diversidade genética por geração
- Detecção de convergência prematura
- Histórico de fitness (melhor + médio)
- Alertas automáticos

---

## Conclusão

**O AG não tem "overfitting" no sentido tradicional** (não é ML supervisionado).

**Mas pode ter:**
1. ✅ **Problema trivial** → Testar com labirintos maiores
2. ✅ **Convergência prematura** → Detectável com `--analyze`
3. ✅ **Parâmetros generosos** → Ajustáveis no código

**Use:** `python test_overfitting.py` para análise completa automática!

