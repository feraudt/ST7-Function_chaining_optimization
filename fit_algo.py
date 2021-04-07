import networkx as nx
import math


def best_fit_nodes(flow, graph_bwd, available_graph) :
    # On trouve le serveur avec le moins de cpu pouvant accueillir chaque fonction
    placed_nodes = []
    for function in flow.nodes() :
        cpu = flow.nodes[function]['cpu']
        cpu_graph = cpu_sous_graph(graph_bwd, cpu)
        place = function_fit(cpu_graph)
        placed_nodes.append((function, {'cpu':cpu, 'func':flow.nodes[function]['func'], 'place':place}))

        # On met à jour le graph physique
        functions = available_graph.nodes[place]['functions']
        if functions == None :
            functions = []
        functions.append(function)
        available_graph.add_node(place, cpu=available_graph.nodes[place]['cpu']-cpu, functions=functions)
        graph_bwd.add_node(place, cpu=graph_bwd.nodes[place]['cpu']-cpu, functions=functions)

    placed_flow = nx.Graph.copy(flow)
    placed_flow.add_nodes_from(placed_nodes)

    return placed_flow


def function_fit(cpu_graph) :
    # Dans le graph avec seulement les serveurs possibles on choisit celui avec le moins de cpu
    min_cpu = math.inf
    place = 0
    for server in cpu_graph.nodes() :
        if cpu_graph.nodes[server]['cpu'] < min_cpu :
            min_cpu = cpu_graph.nodes[server]['cpu']
            place = server
    return server


def cpu_sous_graph(G, cpu_seuil):
    # On note les nodes a supprimer
    nodes_to_delete = []

    for node in G.nodes() :
        if G.nodes[node]['cpu'] <  cpu_seuil :
            nodes_to_delete.append(node)

    # On les supprime de la copie du graph
    F = nx.Graph.copy(G)
    F.remove_nodes_from(nodes_to_delete)

    # On supprime les nodes isoles
    nodes_to_delete = []
    for node in F.nodes() :
        if len(list(F.neighbors(node))) == 0:
            nodes_to_delete.append(node)
    F.remove_nodes_from(nodes_to_delete)

    return F


#def worst_fit_path(placed_flow, graph_bwd, available_graph)

