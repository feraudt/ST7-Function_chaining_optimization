import networkx as nx
import random as rd
from itertools import combinations


def random_connex_graph(nb_nodes, min_edges, range_cpu, range_bandwidth):

    graph = nx.generators.random_graphs.gnm_random_graph(nb_nodes, min_edges)

    for node in graph.nodes:
        cpu = rd.randint(*range_cpu)
        graph.add_node(node, cpu=cpu, functions=[])

    components = nx.connected_components(graph)
    component_combinations = list(combinations(components, 2))

    for couple in component_combinations:
        source = rd.choice(list(couple[0]))
        target = rd.choice(list(couple[1]))
        graph.add_edge(source, target)

    for e in graph.edges:
        bandwidth = rd.randint(*range_bandwidth)
        graph.add_edge(e[0], e[1], bandwidth=bandwidth)

    return graph
