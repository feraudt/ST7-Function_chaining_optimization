from itertools import combinations, groupby
import random as rd
import networkx as nx
import matplotlib.pyplot as plt


def shell_list(nb_nodes, nb_group):
    reste = nb_nodes % nb_group
    slist = [range(k, k + nb_group)
             for k in range(0, nb_nodes - nb_group, nb_group)]
    slist.append(range(nb_nodes - reste, nb_nodes))
    print(slist)
    print("Nodes : ", nb_nodes)
    return slist


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
