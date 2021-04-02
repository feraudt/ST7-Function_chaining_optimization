import networkx as nx
import random as rd
import utils


def generate_request(range_flow, range_node, range_cpu, range_bandwidth):
    # Une requête a une liste de flow (flows), chaque flow est un graphe orienté.
    # Elle a aussi un graphe global (global_graph) qui représente toutes les chaines sur le même graphe
    flows = []
    nb_flow = rd.randint(*range_flow)

    existing_nodes = []
    # Probablilité d'utiliser une node d'une chaine précédente (de relier les deux chaines)
    proba_use_a_previous_node = 0.5

    for flow in range(nb_flow):
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

        flow = utils.generate_flow(nodelist, range_cpu, range_bandwidth)
        flows.append(flow)
        existing_nodes += flow.nodes.data()

    global_graph = nx.DiGraph()
    for f in flows:
        global_graph = nx.compose(global_graph, f)

    return (global_graph, flows)
