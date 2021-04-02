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
    edges = make_connected(nb_nodes, edges)
    for e in edges:
        bandwidth = rd.randint(*range_bandwidth)
        e = (e[0], e[1], {'bandwidth': bandwidth})

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph


def generate_flow(nodelist, range_cpu, range_bandwidth):
    # Genere un flow à partir d'une liste de node, [5,6,7,4] par exemple

    # Construct the list with cpu and bwd
    # func représente le numéro de la fonction virtuelle (utile pour pas relier les flow n'importe comment)
    # par exemple les attributs func de [5,6,7,4] seront [1,2,3,4]
    nodes = [(node, {'cpu': rd.randint(*range_cpu), 'func': i+1})
             for i, node in enumerate(nodelist)]
    bwd = rd.randint(*range_bandwidth)  # Une seule bandwidth par flow
    edges = [(nodelist[i], nodelist[i+1],
              {'bandwidth': bwd}) for i in range(len(nodelist)-1)]

    flow = nx.DiGraph()
    flow.add_nodes_from(nodes)
    flow.add_edges_from(edges)

    return flow


def generate_request(range_flow, range_node, range_cpu, range_bandwidth):
    # Une requête a une liste de flow (flows), chaque flow est un graphe orienté.
    # Elle a aussi un graphe global (global_graph) qui représente toutes les chaines sur le même graphe
    flows = []
    nb_flow = rd.randint(*range_flow)

    existing_nodes = []
    # Probablilité d'utiliser une node d'une chaine précédente (de relier les deux chaines)
    proba_use_a_previous_node = 0.5

    for f
    low in range(nb_flow):
        nb_nodes = rd.randint(*range_node)

        nodelist = []
        for node in range(nb_nodes):
            if len(existing_nodes) > 0 and rd.random() < proba_use_a_previous_node:
                # On choisi une node précédente avec la même func
                possible_nodes = []
                for node in existing_nodes:
                    if node[1]['func'] == len(nodelist)+1:
                        possible_nodes.append(node[0])

                # pas de node possible (si par exemple len(f1)=4 et len(f2)=7)
                if len(possible_nodes) == 0:
                    # On rajoute une nouvelle node, on relie pas
                    nodelist.append(len(existing_nodes) + len(nodelist)+1)
                else:
                    old_node = possible_nodes[rd.randint(
                        0, len(possible_nodes)-1)]
                    nodelist.append(old_node)
            else:
                nodelist.append(len(existing_nodes) +
                                len(nodelist)+1)  # Nouvelle node

        flow = generate_flow(nodelist, range_cpu, range_bandwidth)
        flows.append(flow)
        existing_nodes += flow.nodes.data()

    global_graph = nx.DiGraph()
    for f in flows:
        global_graph = nx.compose(global_graph, f)

    return (global_graph, flows)


def dependance(flows):
