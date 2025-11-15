# **Especificação do Projeto: Agente em Labirinto com Algoritmos de Busca**

## **1\. Objetivo**

Fixar e exercitar conceitos de agentes e algoritmos de busca. O trabalho consiste na simulação de um jogo, no qual um agente deve encontrar a saída de um labirinto.

## **2\. Ambiente: Labirinto**

* O ambiente é uma matriz (grid) n x n.  
* **Entrada (E):** Sempre na posição (0, 0\) e é conhecida pelo agente.  
* **Saída (S):** Pode estar em qualquer posição do labirinto. A posição da saída **não** é conhecida pelo agente e deve ser descoberta.  
* **Paredes:** Representadas pelo caractere 1\.  
* **Caminhos Livres:** Representados pelo caractere 0\.  
* **Arquivos de Entrada:** Serão fornecidos arquivos .txt contendo os labirintos (formato similar ao da *Figura 2* do enunciado original).

## **3\. Movimentação do Agente**

* O agente move-se uma célula de cada vez.  
* **Direções:** 8 direções possíveis (Ortogonais \+ Diagonais):  
  * Cima, Baixo, Esquerda, Direita  
  * Diagonal Esquerda-Cima, Diagonal Direita-Cima  
  * Diagonal Esquerda-Baixo, Diagonal Direita-Baixo  
* **Restrição:** O agente não pode se mover para células de parede (1) nem atravessá-las.

## **4\. Solução (Fases do Processo)**

### **Fase 1: Descoberta da Saída (Algoritmo Genético ou Simulated Annealing)**

* O agente deve encontrar a saída (S) usando um algoritmo de busca com informação por refinamentos sucessivos (ex: **Algoritmo Genético (GA)** ou **Simulated Annealing (SA)**).  
* **Restrição Crítica:** O algoritmo (GA/SA) não conhece a posição de S a priori. Ele deve explorara o labirinto para "tropeçar" nela.  
* **Definições do Aluno:** O aluno deve definir:  
  * A representação do problema (ex: cromossomo no GA).  
  * A função heurística / de avaliação (ex: função de aptidão no GA).  
* **Resultado da Fase 1:** A coordenada (x, y) da Saída S e o caminho que o GA/SA usou para encontrá-la. Este caminho pode não ser o mais curto.

### **Fase 2: Otimização do Caminho (Algoritmo A\*)**

* **Input:** O labirinto completo, a Posição de Entrada E(0, 0\) e a Posição de Saída S(x, y) descoberta na Fase 1\.  
* **Objetivo:** Encontrar o **caminho mais curto** (ideal) entre E e S.  
* **Algoritmo:** Implementar o Algoritmo A\* (extensão do Dijkstra, versão em grafo).

## **5\. Simulação e Visualização**

* A simulação deve exibir informações sobre a execução do algoritmo da Fase 1 (GA/SA).  
* **Modos de Exibição:**  
  * **Modo Rápido:** Exibir o melhor resultado (cromossomo) a cada X gerações.  
  * **Modo Lento:** Exibir informações mais detalhadas do processo.  
* **Saída (Console):**  
  1. Exibir o caminho encontrado pelo GA/SA (da Fase 1).  
  2. Exibir o caminho ótimo encontrado pelo A\* (da Fase 2).  
* **Saída (Arquivo):**  
  * Salvar ambos os caminhos (GA/SA e A\*) em um arquivo de texto, seguindo um formato claro (similar à *Figura 4* do enunciado original).  
* **Entrada (Execução):** O programa deve ser capaz de receber o nome do arquivo de labirinto como argumento de linha de comando (args).

## **6\. Critérios de Avaliação e Entregáveis**

### **6.1. Implementação**

* **Leitura de Arquivo:** Leitura correta do formato de labirinto fornecido.  
* **Algoritmo Genético (GA):**  
  * Implementação completa do ciclo: codificação (cromossomo), seleção, cruzamento (crossover) e mutação.  
  * Definição clara dos critérios de parada.  
  * **Função de Aptidão (Fitness):** Deve ser adequada para o problema, permitindo que o agente *procure* por S sem saber onde ela está. Esta é uma parte fundamental do trabalho.  
* *Algoritmo A:*\*  
  * Implementação correta do A\* para grafos.  
  * Deve receber E e S (descoberta pelo GA) e encontrar o caminho ótimo.  
* **Parâmetros:** A definição e justificativa dos parâmetros do GA (tamanho da população, taxas de mutação/cruzamento, operadores) são importantes.

### **6.2. Entregáveis**

1. **Código Fonte:** Completo e comentado.  
2. **Executável:** Um executável ou script de fácil execução (ex: python main.py labirinto1.txt).  
3. **Arquivos de Saída:** Os arquivos .txt de solução gerados para os labirintos de teste fornecidos.  
4. **Relatório (PPT):**  
   * Explicando a codificação do GA, tamanho da população, função de aptidão/heurística.  
   * Operadores de GA escolhidos, taxas de mutação e cruzamento.  
   * Problemas encontrados e considerações sobre o desenvolvimento.  
5. **Apresentação:** O trabalho deve ser apresentado.

***Nota:** As "Figuras" (1, 2, 3, 4\) mencionadas no texto original não foram fornecidas, mas a descrição é suficiente para inferir os formatos de entrada e saída esperados.*

