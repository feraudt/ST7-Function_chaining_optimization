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
    func_list = list(placed_flow.nodes())
    # On note la suite des serveurs par lesquels passe la chaine avec les fonctions placees (0 si pas de fonction)
    path_servers = [(placed_flow.nodes[func_list[0]]['place'], func_list[0])]
    for k in range(len(func_list)-1) :
        if placed_flow.nodes[func_list[k]]['place'] == placed_flow.nodes[func_list[k+1]]['place'] :
            path_servers.append((placed_flow.nodes[func_list[k+1]]['place'], func_list[k+1]))
        else :
            chemin = paths_to_function(func_list[k], func_list[k+1], bwd, placed_flow, graph_bwd, available_graph)
            path_servers += chemin

    # Affichage
    for tuple in path_servers :
        print('Server {} : function {}'.format(*tuple))
    return path_servers


def paths_to_function(start_func, end_func, bwd, placed_flow, graph_bwd, available_graph) :
    end_server = placed_flow.nodes[end_func]['place']
    nodes_by_step = [{placed_flow.nodes[start_func]['place']: {'parent':None, 'nb_edges':0, 'min_bwd':math.inf, 'function': start_func}}]

    # Parcours en largeur jusqu'a trouver le server cible
    while end_server not in nodes_by_step[-1].keys() :
        accessible_servers = {}
        for server in nodes_by_step[-1].keys() :
            neighbors = list(graph_bwd.adj[server])
            for adj_node in neighbors :
                min_bwd = min(nodes_by_step[-1][server]['min_bwd'], graph_bwd.edges[server, adj_node]['bandwidth'] - bwd)
                if adj_node == end_server :
                    funct = end_func
                else : funct = 0
                if adj_node not in accessible_servers.keys() :
                    if adj_node not in nodes_by_step[-1].keys() :
                        accessible_servers[adj_node] = {'parent':server, 'nb_edges':nodes_by_step[-1][server]['nb_edges']+1, 'min_bwd':min_bwd, 'function':funct}
                    elif min_bwd > nodes_by_step[-1][adj_node]['min_bwd']+1 :
                        accessible_servers[adj_node] = {'parent':server, 'nb_edges':nodes_by_step[-1][server]['nb_edges']+1, 'min_bwd':min_bwd, 'function':funct}
                elif min_bwd > accessible_servers[adj_node]['min_bwd'] :
                    accessible_servers[adj_node] = {'parent':server, 'nb_edges':nodes_by_step[-1][server]['nb_edges']+1, 'min_bwd':min_bwd, 'function':funct}
        nodes_by_step.append(accessible_servers)
    # On cherche une derniere fois pour prendre en compte les chemins plus longs de 1 qui seraient plus performants
    accessible_servers = {}
    for server in nodes_by_step[-1].keys() :
        neighbors = list(graph_bwd.adj[server])
        for adj_node in neighbors :
            min_bwd = min(nodes_by_step[-1][server]['min_bwd'], graph_bwd.edges[server, adj_node]['bandwidth'] - bwd)
            if adj_node == end_server :
                funct = end_func
            else : funct = 0
            if adj_node not in accessible_servers.keys() :
                if adj_node not in nodes_by_step[-1].keys() :
                    accessible_servers[adj_node] = {'parent':server, 'nb_edges':nodes_by_step[-1][server]['nb_edges']+1, 'min_bwd':min_bwd, 'function':funct}
                elif min_bwd > nodes_by_step[-1][adj_node]['min_bwd']+1 :
                    accessible_servers[adj_node] = {'parent':server, 'nb_edges':nodes_by_step[-1][server]['nb_edges']+1, 'min_bwd':min_bwd, 'function':funct}
            elif min_bwd > accessible_servers[adj_node]['min_bwd'] :
                accessible_servers[adj_node] = {'parent':server, 'nb_edges':nodes_by_step[-1][server]['nb_edges']+1, 'min_bwd':min_bwd, 'function':funct}

    if end_server in nodes_by_step[-1].keys() :
        chemin = get_path(nodes_by_step.reverse(), end_server, bwd, available_graph)
    else : chemin = get_path(nodes_by_step[:(len(nodes_by_step)-1)].reverse(), end_server, bwd, available_graph)
    return chemin


def get_path(rev_by_step, end_server, bwd, available_graph) :
    chemin = [(end_server, rev_by_step[0][end_server]['function'])]
    for k in range(len(rev_by_step)-1) :
        parent = rev_by_step[k][chemin[-1][0]]['parent']
        edge_attr = available_graph.edges[parent, chemin[-1][0]]
        new_edge = (parent, chemin[-1][0], {'bandwidth': edge_attr['bandwidth'] - bwd})
        available_graph.add_edge(*new_edge)
        if k < len(rev_by_step) - 2 :
            chemin.append((parent, rev_by_step[k+1][parent]['function']))
    return chemin.reverse()















