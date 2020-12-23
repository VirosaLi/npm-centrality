from json import load

import networkx as nx

from utils import build_complete_graph

dep_graph = build_complete_graph()

with open("../data/wallet.json", "r") as file:
    seed = load(file)
del seed["blockchain/unused-My-Wallet"]

seed_role = {key: "seed" for key in seed.keys()}
leaf_role = {module: "leaf" for module, out_degree in dep_graph.out_degree if out_degree == 0}
seed_leaf = {**seed_role, **leaf_role}
inter_role = {module: "intermediate" for module in dep_graph.nodes if module not in seed_leaf}
role_dict = {**seed_leaf, **inter_role}

nx.set_node_attributes(dep_graph, role_dict, "role")

nx.write_gml(dep_graph, "../data/dep_graph_role.gml")
