from itertools import combinations, groupby
import random as rd
import networkx as nx
import matplotlib.pyplot as plt


def get_node_cluster(start_node, nb_nodes, edges):
    cluster = [start_node]
    for node in cluster:
        for e in edges:
            if e[0] == node and e[1] not in cluster:
                cluster.append(e[1])
            elif e[1] == node and e[0] not in cluster:
                cluster.append(e[0])
    return sorted(cluster)


def connected_nodes(clusters):
    total_nodes = 0
    for cluster in clusters:
        total_nodes += len(cluster)
    return total_nodes


def make_connected(nb_nodes, edges):
    clusters = [get_node_cluster(1, nb_nodes, edges)]

    i = 2
    while i < nb_nodes + 1 and connected_nodes(clusters) < nb_nodes:
        connected = False
        for cluster in clusters:
            if i in cluster:
                connected = True
        if not connected:
            clusters.append(get_node_cluster(i, nb_nodes, edges))
        i += 1

    n = len(clusters)
    if n == 1:
        return edges
    else:
        for i in range(n-1):
            for j in range(i+1, n):
                n1 = rd.randint(0, len(clusters[i]))
                n2 = rd.randint(0, len(clusters[j]))
                edges.append((n1, n2))
    return edges


def make_connex(G):
    components = dict(enumerate(nx.connected_components(G)))
    components_combs = combinations(components.keys(), r=2)

    for _, node_edges in groupby(components_combs, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_comps = rd.choice(node_edges)
        source = rd.choice(list(components[random_comps[0]]))
        target = rd.choice(list(components[random_comps[1]]))
        G.add_edge(source, target)

    return G


def generate_flow(nodelist, range_cpu, range_bandwidth):
    # Genere un flow à partir d'une liste de node, [5,6,7,4] par exemple

    # Construct the list with cpu and bwd
    # func représente le numéro de la fonction virtuelle (utile pour pas relier les flow n'importe comment)
    # par exemple les attributs func de [5,6,7,4] seront [1,2,3,4]
    nodes = [(node, {'cpu': rd.randint(*range_cpu), 'func': i+1})
             for i, node in enumerate(nodelist)]
    edges = [(nodelist[i], nodelist[i+1],
              {'bandwidth': rd.randint(*range_bandwidth)}) for i in range(len(nodelist)-1)]

    flow = nx.DiGraph()
    flow.add_nodes_from(nodes)
    flow.add_edges_from(edges)

    return flow