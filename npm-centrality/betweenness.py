from networkx.algorithms import betweenness_centrality

from utils import build_complete_graph


dep_graph = build_complete_graph()

betw = betweenness_centrality(dep_graph)
betw = sorted(betw.items(), key=lambda x: x[1], reverse=True)

num_package = 13
for package, betw_score in betw[:num_package]:
    print(f"{package}, {betw_score:.6f}")
