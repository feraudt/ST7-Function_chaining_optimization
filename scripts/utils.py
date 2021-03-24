from itertools import combinations, groupby
import random as rd
import networkx as nx
import matplotlib.pyplot as plt

def get_node_cluster(start_node, nb_nodes, edges) :
    cluster = [start_node]
    for node in cluster :
        for e in edges :
            if e[0] == node and e[1] not in cluster :
                cluster.append(e[1])
            elif e[1] == node and e[0] not in cluster :
                cluster.append(e[0])
    return sorted(cluster)

def connected_nodes(clusters) :
    total_nodes = 0
    for cluster in clusters :
        total_nodes += len(cluster)
    return total_nodes

def make_connected(nb_nodes, edges) :
    clusters = [get_node_cluster(1, nb_nodes, edges)]

    i = 2
    while i < nb_nodes + 1 and connected_nodes(clusters) < nb_nodes :
        connected = False
        for cluster in clusters :
            if i in cluster :
                connected = True
        if not connected :
            clusters.append(get_node_cluster(i, nb_nodes, edges))
        i += 1

    n = len(clusters)
    if n == 1 :
        return edges
    else :
        for i in range(n-1) :
            for j in range(i+1, n) :
                n1 = rd.randint(len(clusters[i]))
                n2 = rd.randint(len(clusters[j]))
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


def shell_list(nb_nodes, nb_group):
    reste = nb_nodes % nb_group
    slist = [range(k, k + nb_group) for k in range(0, nb_nodes - nb_group, nb_group)]
    slist.append(range(nb_nodes - reste, nb_nodes))
    print(slist)
    print("Nodes : ", nb_nodes)
    return slist


def plot_graph(G):
    plt.plot()
    nx.draw(G, with_labels=True)
    plt.show()

def random_connex_graph(nb_nodes, min_edges, range_cpu, range_bandwidth) :
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
    edges = make_connected(nb_nodes, edges)
    for e in edges :
        bandwidth = rd.randint(*range_bandwidth)
        e = (e[0], e[1], {'bandwidth': bandwidth})

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph












