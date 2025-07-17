# Projeto Final - Citate Network Cora

## O que é o Dataset?

O Dataset contém 2.708 artigos científicos na área de machine learning, classificados em 7 categorias (ex: Neural Networks, Genetic Algorithms), a rede de citações presentes nos artigos possui 5.429 ligações direcionadas, onde cada aresta representa “A cita B”. Assim cada artigo é descrito por um vetor binário de 1.433 termos (0/1) que representa a presença de palavras no texto.

## O que são os nós e as arestas?

Os nós se tratam de cada artigo, identificado por um paper_id, com atributos: vetor de características (1433 dimensões) e o rótulo de categoria (1 das 7 classes).
As arestas se tratam de direções apontando de um paper que cita para o citado (rede direcionada).

#### Devido o grafo não ser conectado, foi criado um subgrafo conectado com 2485 nós

