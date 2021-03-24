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


def bwd_sous_graph(G, bwd_seuil):
    # On note les edge à supprimer
    edge_to_delete = []
    for u, v in G.edges():
        if G.edges[u, v]['bandwidth'] < bwd_seuil:
            edge_to_delete.append((u, v))
    F = nx.Graph.copy(G)

    # On les supprime de F
    F.remove_edges_from(edge_to_delete)

    # On enlève les sommets seuls
    node_to_delete = []
    for node in F.nodes():
        if len(list(F.neighbors(node))) == 0:
            node_to_delete.append(node)
    F.remove_nodes_from(node_to_delete)

    return F
