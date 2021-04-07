import networkx as nx
import math
from utils import *


def best_fit_nodes(flow, available_graph) :
    # On travaille sur un sous graphe en bwd:
    bwd = get_bwd(flow)
    graph_bwd = bwd_sous_graph(available_graph, bwd)
    # On trouve le serveur avec le moins de cpu pouvant accueillir chaque fonction
    placed_nodes = []
    placed_funcs = placed_functions(graph_bwd)
    for function in flow.nodes() :
        if function in placed_funcs.keys() :
            place = placed_funcs[function]
            cpu = flow.nodes[function]['cpu']
            placed_nodes.append((function, {'cpu':cpu, 'func':flow.nodes[function]['func'], 'place':place}))
        else :
            cpu = flow.nodes[function]['cpu']
            place = function_fit(function, cpu, graph_bwd)
            placed_nodes.append((function, {'cpu':cpu, 'func':flow.nodes[function]['func'], 'place':place}))

            # On met à jour le graph physique si la fonction a ete ajoutee
            functions = available_graph.nodes[place]['functions']
            if functions == None :
                functions = []
            functions.append(function)
            available_graph.add_node(place, cpu=available_graph.nodes[place]['cpu']-cpu, functions=functions)
            graph_bwd.add_node(place, cpu=graph_bwd.nodes[place]['cpu']-cpu, functions=functions)

    placed_flow = nx.Graph.copy(flow)
    placed_flow.add_nodes_from(placed_nodes)

    # On affiche le placement
    flow_view = []
    servers_view = []
    for func in placed_nodes :
        flow_view.append(func[0])
        servers_view.append(func[1]['place'])
    print('Functions : ', flow_view)
    print('Servers : ', servers_view)

    return placed_flow


def function_fit(function, cpu, graph_bwd) :
    cpu_graph = cpu_sous_graph(graph_bwd, cpu)
    # Dans le graph avec seulement les serveurs possibles on choisit celui avec le moins de cpu
    min_cpu = math.inf
    place = 0
    for server in cpu_graph.nodes() :
        if cpu_graph.nodes[server]['cpu'] < min_cpu :
            min_cpu = cpu_graph.nodes[server]['cpu']
            place = server
    return place


def placed_functions(graph_bwd) :
    placed_funcs = {}
    # On note les fonctions deja placees
    for node in graph_bwd.nodes() :
        if graph_bwd.nodes[node]['functions'] != None :
            for func in graph_bwd.nodes[node]['functions'] :
                placed_funcs[func] = node
    print('Already placed functions : ', placed_funcs)
    return placed_funcs



def worst_fit_path(placed_flow, available_graph) :
    bwd = get_bwd(placed_flow)
    graph_bwd = bwd_sous_graph(available_graph, bwd)
    path_servers = []


def paths_to_function(start_func, end_func, bwd, graph_bwd) :
    nodes_by_step = [{graph_bwd.nodes[start-func]['place']: {'parent':None, 'nb_edges':0, 'min_bwd':math.inf}}]














