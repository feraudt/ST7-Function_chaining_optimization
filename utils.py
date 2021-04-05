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


def plot_graph(G, title=''):
    plt.plot()
    plt.title(title)
    nx.draw(G, pos=nx.kamada_kawai_layout(G), with_labels=True)
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


def dependance(flows):
    total_nodes = [node for f in flows for node in list(f)]
    # doublons = liste des nodes qui connectent les flows
    doublons = list(
        set([node for node in total_nodes if total_nodes.count(node) > 1]))

    # = [(noeud,[flow1,flow2]) , ... ] si flow1 et flow2 sont connectés
    dependant_flow = []
    isdependant = []  # liste des chaines dépendantes afin d'obtenir les indépendantes plus bas
    for noeud in doublons:
        dependant_flow.append((noeud, []))
        for f in flows:
            if noeud in list(f):
                if f not in isdependant:
                    isdependant.append(f)
                dependant_flow[-1][1].append(f)

    independant_flow = [f for f in flows if f not in isdependant]

    return (dependant_flow, independant_flow)


def flow_sort(flows):
    # Trie les chaines par bandwidth décroissante
    # La key lambda va chercher la bwd du premier edge
    return sorted(flows, key=lambda f: list(flows[0].edges(data=True))[0][2]['bandwidth'], reverse=True)
