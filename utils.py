from itertools import combinations, groupby
import random as rd
import networkx as nx
import matplotlib.pyplot as plt
import math
import os


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


def save_graph(G, title='', chemin='fig/'):
    if not os.path.isdir(chemin):
        os.makedirs(chemin)
    fig = plt.figure()
    plot_graph(G, title)
    fig.savefig(chemin + title + '.png')


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

    # Retourne la plus grande composante connexe
    F = F.subgraph(max(nx.connected_components(F), key=len)).copy()
    return F


def get_common_nodes(flows):
    # Retourne une liste contenant pour chaque flow dans flows la liste des noeuds en commun

    total_nodes = [node for f in flows for node in list(f)]
    # doublons = liste des nodes qui connectent les flows
    doublons = list(
        set([node for node in total_nodes if total_nodes.count(node) > 1]))

    return [[noeud for noeud in doublons if noeud in flow] for flow in flows]


def dependance(flow, flows):
    # Renvoie les noeuds de flow présent dans flows (il ne faut pas que flow appartienne à flows du coup)
    total_nodes = [node for f in flows for node in list(f)]
    return [node for node in flow if node in total_nodes]


def get_bwd(flow):
    return list(flow.edges(data=True))[0][2]['bandwidth']


def flow_sort(flows):
    # Trie les chaines par bandwidth décroissante
    # La key lambda va chercher la bwd du premier edge
    return sorted(flows, key=lambda f: get_bwd(f), reverse=True)


def cpu_sous_graph(G, cpu_seuil):
    # On note les nodes a supprimer
    nodes_to_delete = []

    for node in G.nodes():
        if G.nodes[node]['cpu'] < cpu_seuil:
            nodes_to_delete.append(node)

    # On les supprime de la copie du graph
    F = nx.Graph.copy(G)
    F.remove_nodes_from(nodes_to_delete)

    # On supprime les nodes isoles
    nodes_to_delete = []
    for node in F.nodes():
        if len(list(F.neighbors(node))) == 0:
            nodes_to_delete.append(node)
    F.remove_nodes_from(nodes_to_delete)

    return F


def find_origin_chain(flow):
    functions = [func for func in flow.nodes()]
    for fr, to in flow.edges() :
        functions.remove(to)











