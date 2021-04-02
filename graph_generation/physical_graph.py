import networkx as nx
import random as rd
import utils

def random_connex_graph(nb_nodes, min_edges, range_cpu, range_bandwidth):
    nodes = []
    edges = []

    for i in range(nb_nodes):
        cpu = rd.randint(*range_cpu)
        nodes.append((i+1, {'cpu': cpu}))

    for i in range(min_edges):
        s1 = rd.randint(1, nb_nodes)
        s2 = rd.randint(1, nb_nodes)
        while s2 == s1:
            s2 = rd.randint(1, nb_nodes)
        edges.append((s1, s2))

    edges = list(set(edges))
    edges = utils.make_connected(nb_nodes, edges)
    for e in edges:
        bandwidth = rd.randint(*range_bandwidth)
        e = (e[0], e[1], {'bandwidth': bandwidth})

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph