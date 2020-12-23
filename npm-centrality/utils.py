from json import load, dump

from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from networkx.algorithms import betweenness_centrality
from tqdm import tqdm

from criticality import fetch_criticality


def build_graph_from_dict(data_dict):
    g = nx.DiGraph()
    for package, deps in data_dict.items():
        g.add_node(package)
        for dep in deps:
            g.add_edge(package, dep)
    return g


def seq_to_dist(sequence):
    unique, counts = np.unique(sequence, return_counts=True)
    counts_map = np.asarray((unique, counts)).T
    return counts_map[:, 1] / np.sum(counts_map[:, 1])


def build_complete_graph():
    with open("../data/wallet_complete_with_failed.json", "r") as file:
        data = load(file)

    dep_graph = build_graph_from_dict(data)

    with open("../data/wallet.json", "r") as file:
        data = load(file)

    for package, deps in data.items():
        dep_graph.add_node(package)
        for dep in deps:
            dep_graph.add_edge(package, dep)

    dep_graph.remove_node("blockchain/unused-My-Wallet")
    return dep_graph


if __name__ == "__main__":
    graph = build_complete_graph()

    betw = betweenness_centrality(graph)
    betw = sorted(betw.items(), key=lambda x: x[1], reverse=True)

    with open("../data/wallet_url_improved.json", "r") as file:
        urls = load(file)

    results = []
    for package, betw_score in tqdm(betw[100:200]):
        cs = 0 if package not in urls else fetch_criticality(package)
        results.append({"name": package, "betw": betw_score, "cs": cs})

    with open("../data/wallet_criticality_100-200.json", "w") as file:
        dump(results, file, indent=4)

    # nx.write_gml(dep_graph, "../data/dep_graph.gml")

    # print(dep_graph.number_of_nodes())
    # print(nx.number_weakly_connected_components(dep_graph))
    # print(nx.is_weakly_connected(dep_graph))
    # weak_comp = nx.weakly_connected_components(dep_graph)
    # for comp in weak_comp:
    #     print(comp)
    # print(dep_graph.number_of_nodes())
    # print(dep_graph.number_of_edges())
    # print("blockchain/unused-My-Wallet" in data)

    # in_degree_sequence = [degree for _, degree in dep_graph.in_degree()]
    # out_degree_sequence = [degree for _, degree in dep_graph.out_degree()]
    # in_deg_dist = seq_to_dist(in_degree_sequence)
    # out_deg_dist = seq_to_dist(out_degree_sequence)
    # _, ax = plt.subplots()
    # ax.loglog(in_deg_dist, 'r.', label='In-degree')
    # ax.loglog(out_deg_dist, 'b.', label='Out-degree')
    # ax.legend(loc='upper right', shadow=True, fontsize='x-large')
    # plt.title('Degree Distribution')
    # plt.xlabel('degree')
    # plt.ylabel('frequency')
    # plt.show()
