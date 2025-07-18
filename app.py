from pathlib import Path
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import community as community_louvain
from networkx.algorithms import link_prediction

st.set_page_config(layout="wide")
st.title("Network Analysis on Cora + Simulações")

@st.cache_data
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

part = community_louvain.best_partition(G.to_undirected() if G.is_directed() else G)

# Criar visualização interativa
net = Network(height="500px", width="100%", notebook=False, cdn_resources="in_line")
for node in G.nodes():
    net.add_node(node, label=str(node), color=f"hsl({part[node]*57 % 360}, 70%, 60%)")

for source, target in G.edges():
    net.add_edge(source, target)

net.toggle_physics(True)
net.show_buttons(filter_=["physics"])
net.save_graph('graph.html')
html = open('graph.html', 'r', encoding='utf-8').read()
st.subheader("🔍 Visualização Interativa da Rede")
st.components.v1.html(html, height=550)

st.subheader("📊 Estatísticas da Rede")
st.write(f"- **Nós:** {G.number_of_nodes()} | **Arestas:** {G.number_of_edges()}")
st.write(f"- **Densidade:** {nx.density(G):.4f}")

try:
    if G.is_directed():
        GC = G.subgraph(max(nx.weakly_connected_components(G), key=len))
        diameter = nx.diameter(GC.to_undirected())
    else:
        GC = G.subgraph(max(nx.connected_components(G), key=len))
        diameter = nx.diameter(GC)
    st.write(f"- **Diâmetro:** {diameter}")
except:
    st.warning("Grafo desconectado ou muito pequeno para calcular diâmetro.")

clu_avg = nx.average_clustering(G.to_undirected() if G.is_directed() else G)
st.write(f"- **Clustering Global:** {clu_avg:.4f}")

st.subheader("🏆 Nós Mais Centrais")
deg = nx.degree_centrality(G)
clo = nx.closeness_centrality(G)
bet = nx.betweenness_centrality(G)
try:
    eigen = nx.eigenvector_centrality(G, max_iter=500)
except:
    eigen = {k: 0 for k in G.nodes()}

for name, centrality in zip(["Degree", "Closeness", "Betweenness", "Eigenvector"],
                            [deg, clo, bet, eigen]):
    top = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    st.write(f"**{name}**: " + ", ".join([f"{i}:{v:.3f}" for i, v in top]))

st.subheader("🧩 Comunidades (Louvain)")
st.write(f"- Número de comunidades: {len(set(part.values()))}")
st.write(f"- Modularidade: {community_louvain.modularity(part, G.to_undirected() if G.is_directed() else G):.4f}")

st.subheader("📈 Distribuição de Grau")
deglist = [d for _, d in G.degree()]
st.bar_chart(pd.Series(deglist).value_counts().sort_index())

st.subheader("🛡️ Resiliência da Rede")
frac = st.sidebar.slider("Fração de nós removida (por grau)", 0.0, 0.5, 0.1)
G2 = G.copy()
top = sorted(G2.degree(), key=lambda x: x[1], reverse=True)
rem = [n for n, _ in top[:int(frac * len(top))]]
G2.remove_nodes_from(rem)
try:
    GC_size = len(max(nx.connected_components(G2.to_undirected() if G2.is_directed() else G2), key=len))
    st.write(f"Após remover {frac*100:.0f}% dos nós de maior grau → Tamanho da GC: {GC_size}")
except:
    st.warning("Erro ao calcular componente gigante após remoção.")

st.subheader("🔗 Link Prediction (Jaccard)")
try:
    preds = list(link_prediction.jaccard_coefficient(G))
    top5 = sorted(preds, key=lambda x: x[2], reverse=True)[:5]
    st.write("Top-5 potenciais links:")
    for u, v, p in top5:
        st.write(f"{u} – {v} → {p:.3f}")
except:
    st.warning("Erro ao calcular previsão de links.")
