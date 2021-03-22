from itertools import combinations, groupby
import random
import networkx as nx
import matplotlib.pyplot as plt


def make_connex(G):
    components = dict(enumerate(nx.connected_components(G)))
    components_combs = combinations(components.keys(), r=2)

    for _, node_edges in groupby(components_combs, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_comps = random.choice(node_edges)
        source = random.choice(list(components[random_comps[0]]))
        target = random.choice(list(components[random_comps[1]]))
        G.add_edge(source, target)

    return G


def plot_graph(G):
    plt.plot()
    nx.draw(G, with_labels=True)
    plt.show()
