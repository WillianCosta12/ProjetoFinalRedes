from pathlib import Path
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import community as community_louvain
from networkx.algorithms import link_prediction

st.set_page_config(layout="wide")
st.title("Network Analysis on Cora + Simulations")

def load_cora():
    base = Path(__file__).parent
    cites_fp = base / "data" / "cora.cites"
    df = pd.read_csv(cites_fp, sep='\t', header=None, names=["target", "source"])
    G = nx.from_pandas_edgelist(df, source="source", target="target", create_using=nx.DiGraph())
    return G

G_cora = load_cora()
n = G_cora.number_of_nodes()

model = st.sidebar.selectbox("Rede", ["Cora", "Erdos-Renyi", "Watts-Strogatz", "Barabasi-Albert"])
G = {
    "Cora": G_cora,
    "Erdos-Renyi": nx.erdos_renyi_graph(n, p=0.01),
    "Watts-Strogatz": nx.watts_strogatz_graph(n, k=4, p=0.1),
    "Barabasi-Albert": nx.barabasi_albert_graph(n, m=2)
}[model]

st.sidebar.write(f"### Modelo: {model}")

net = Network(height="500px", width="100%", notebook=False)
net.from_nx(G)
net.toggle_physics(True)
net.show_buttons(filter_=['physics'])
net.save_graph('graph.html')
html = open('graph.html','r', encoding='utf-8').read()
st.subheader("Visão da Rede")
st.components.v1.html(html, height=550)

st.subheader("📊 Estatísticas da Rede")
st.write(f"- **Nós:** {G.number_of_nodes()} | **Arestas:** {G.number_of_edges()}")
st.write(f"- **Densidade:** {nx.density(G):.4f}")

if G.number_of_nodes() == 0:
    st.warning("Grafo vazio — impossível calcular conectividade ou diâmetro.")
else:
    if G.is_directed():
        if nx.is_weakly_connected(G):
            GC = G.subgraph(max(nx.weakly_connected_components(G), key=len))
            di = nx.diameter(GC.to_undirected())
        else:
            st.warning("Grafo dirigido não é fracamente conectado")
            di = None
    else:
        if nx.is_connected(G):
            GC = G
        else:
            GC = G.subgraph(max(nx.connected_components(G), key=len))
        di = nx.diameter(GC)
    st.write(f"Diâmetro: {di}")

if nx.is_connected(G):
    di = nx.diameter(G)
    st.write(f"- **Diâmetro:** {di}")
else:
    GC = G.subgraph(max(nx.connected_components(G), key=len))
    st.write(f"- **Não conectada:** tomando gigante componente → Diâmetro = {nx.diameter(GC)}")

clu_avg = nx.average_clustering(G)
st.write(f"- **Clustering global:** {clu_avg:.4f}")

st.subheader("🔝 Nós mais importantes por Centralidade")
deg = nx.degree_centrality(G)
clo = nx.closeness_centrality(G)
bet = nx.betweenness_centrality(G)
eigen = nx.eigenvector_centrality(G, max_iter=500)

for name, centrality in zip(["Degree", "Closeness", "Betweenness", "Eigenvector"],
                            [deg, clo, bet, eigen]):
    vals = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    st.write(f"**{name}**: " + ", ".join([f"{i}:{v:.3f}" for i,v in vals]))

st.subheader("🧩 Comunidades - Método Louvain")
part = community_louvain.best_partition(G)
mod = community_louvain.modularity(part, G)
st.write(f"- Número de comunidades: {len(set(part.values()))}")
st.write(f"- Modularidade: {mod:.4f}")

st.subheader("📈 Distribuição de Grau")
deglist = [d for _, d in G.degree()]
st.bar_chart(pd.Series(deglist).value_counts().sort_index())

st.subheader("🛡️ Resiliência da Rede")
frac = st.sidebar.slider("Fração de nós removida (por grau)", 0.0, 0.5, 0.1)
G2 = G.copy()
top = sorted(G2.degree(), key=lambda x: x[1], reverse=True)
rem = [n for n,_ in top[:int(frac*len(top))]]
G2.remove_nodes_from(rem)
gc_size = len(max(nx.connected_components(G2), key=len))
st.write(f"Após remover {frac*100:.0f}% nós de maior grau → tamanho da GC = {gc_size}")

st.subheader("🔗 Link Prediction (heurística)")
node_pairs = list(link_prediction.jaccard_coefficient(G))
top5 = sorted(node_pairs, key=lambda x: x[2], reverse=True)[:5]
st.write("Top-5 potenciais links (Jaccard):")
for u, v, score in top5:
    st.write(f"{u} – {v} → {score:.3f}")
