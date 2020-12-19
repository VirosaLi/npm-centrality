from json import load

from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from networkx.algorithms import betweenness_centrality


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


if __name__ == '__main__':
    with open("../data/wallet_url.json", "r") as file:
        data = load(file)

    print(len(data))

    # with open("../data/wallet_complete_with_failed.json", "r") as file:
    #     data = load(file)
    #
    # dep_graph = build_graph_from_dict(data)
    #
    # with open("../data/wallet.json", "r") as file:
    #     data = load(file)
    #
    # print(len(data))
    # for package, deps in data.items():
    #     dep_graph.add_node(package)
    #     for dep in deps:
    #         dep_graph.add_edge(package, dep)
    #
    # dep_graph.remove_node("blockchain/unused-My-Wallet")

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
