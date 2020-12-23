from json import load

from matplotlib import pyplot as plt
import numpy as np


with open("../data/wallet_criticality_top100.json", "r") as file:
    cs_100 = load(file)

with open("../data/wallet_criticality_100-200.json", "r") as file:
    cs_200 = load(file)


cs_data = cs_100 + cs_200

cs_score = [e["cs"] for e in cs_data]
betw = [e["betw"] for e in cs_data]

y = np.array(cs_score)
y[y == 0] = y.mean()
y_sort_arg = np.argsort(y)
y[y_sort_arg[0]] = y[y_sort_arg[1]]

threshold = 0.18
upper = np.ma.masked_where(y <= threshold, y)
lower = np.ma.masked_where(y > threshold, y)

_, ax = plt.subplots()
ax.hlines(threshold, 0, np.min(y) / 200, "k", linestyles="dashed")
ax.plot(betw, upper, "bo", betw, lower, "ro")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Betweenness")
plt.ylabel("Criticality Score")
plt.title("Criticality Score v.s. Betweenness Centrality ")
# place a text box in upper left in axes coords
props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
ax.text(
    0.65,
    0.65,
    f"threshold={threshold}",
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment="top",
    bbox=props,
)
plt.show()
