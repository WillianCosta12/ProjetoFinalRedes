# Projeto Final - Citate Network Cora

## O que é o Dataset?

O Dataset contém 2.708 artigos científicos na área de machine learning, classificados em 7 categorias (ex: Neural Networks, Genetic Algorithms), a rede de citações presentes nos artigos possui 5.429 ligações direcionadas, onde cada aresta representa “A cita B”. Assim cada artigo é descrito por um vetor binário de 1.433 termos (0/1) que representa a presença de palavras no texto.

### O que são os nós e as arestas?

Os nós se tratam de cada artigo, identificado por um paper_id, com atributos: vetor de características (1433 dimensões) e o rótulo de categoria (1 das 7 classes).
As arestas se tratam de direções apontando de um paper que cita para o citado (rede direcionada).

#### Devido o grafo não ser conectado, foi criado um subgrafo conectado com 2485 nós

### Matriz de adjacência
Matriz adjacência: (2485, 2485)

### Diâmetro e periferia da rede
Diâmetro da rede: 19
Nós na periferia: [2462, 2513]

### Esparsidade/Densidade e Assortatividade geral da rede
Densidade da rede: 0.001642
Coeficiente de assortatividade (grau): -0.071365

### Histograma de distribuição empírica de grau
![Histograma](/imagens/Histograma.png)

### Valores
- Clustering local: {0: 0.3333333333333333, 1: 0, 2: 0, 4: 0.7}
- Média dos clustering locais: 0.2376
- Clustering global (transitividade): 0.0900
- Strongly connected? False
- Weakly connected? False
- Número de SCC: 78
- Número de WCC: 78

### Visualização para exibir os nós mais importantes
![Degree Centrality](/imagens/degreeCentrality.png)
![Eigenvector Centrality](/imagens/eigenvectorCentrality.png)
![Closeness Centrality](/imagens/closenessCentrality.png)
![Betweenness Centrality](/imagens/betweennessCentrality.png)

### Detecção de comunidades/partições
![Método Louvain](/imagens/metodoLouvain.png)
Modularidade obtida: 0.8053
Níveis disponíveis: 4

### Visualização pelo Pyvis
Link: https://williancosta12.github.io/ProjetoFinalRedes/cora

### Visualização pelo StreamLit
Link: https://projetofinalredes-66gm5r8vzbzyug5gpj3jfv.streamlit.app
