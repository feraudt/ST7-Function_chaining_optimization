# Dependencies

import networkx as nx
from networkx.algorithms import approximation as nxa
import random as rd
import time
import os
import shutil
import copy

import graph_generation
from utils import *
from fit_algo import *

# On supprime les figures existantes:
dir = 'fig/'
if not os.path.exists(dir):
    os.makedirs(dir)
for files in os.listdir(dir):
    path = os.path.join(dir, files)
    try:
        shutil.rmtree(path)
    except OSError:
        os.remove(path)

# Graphe Physique
nb_server = rd.randint(10, 20)
# nombre max de lien = n(n-1)/2
min_link = rd.randint(nb_server-1, int(nb_server*(nb_server-1)/4))
range_cpu = (5, 10)
range_bandwidth = (7, 15)

physical_graph = graph_generation.random_connex_graph(
    nb_server, min_link, range_cpu, range_bandwidth)

# Affichage
save_graph(physical_graph, 'Graphe Physique', bwd=True, cpu=True)


# Graphe Virtuel

# v de vrange est pour virtuel (pour pas mélanger)
vrange_flow = (2, 3)
vrange_node = (4, 7)
vrange_cpu = (1, 5)
vrange_bandwidth = (5, 10)
# Probablilité d'utiliser une node d'une chaine précédente (de relier les deux chaines)
proba_dependance = 0.5

(global_graph, flows) = graph_generation.generate_request(
    vrange_flow, vrange_node, vrange_cpu, vrange_bandwidth, proba_dependance)

# On trie les chaines par bwd décroissante
flows = flow_sort(flows)

# Affichage des flows un par un et de la requête
for i, f in enumerate(flows):
    name = 'Flow {} '.format(i+1)
    save_graph(f, name, 'fig/Virtual_Graph/')
if len(flows) > 1:
    save_graph(global_graph, 'Graphe Virtuel',
               'fig/Virtual_Graph/', bwd=True, cpu=True)

#################################
# Implémentation du Pseudo-Code #
#################################
# Place les chaines sans utiliser les steiner trees


available_graph = copy.deepcopy(physical_graph)
placed_flows = []
chemins = []
placed_physical_flows = []
fig_chemin = 'fig/Flows/'

for flow in flows:
    # Variables pour les figures
    flow_id = flows.index(flow)+1
    flow_name = 'Flow {}'.format(flow_id)
    print('\n'+flow_name)

    placed_flow = best_fit_nodes(flow, available_graph)
    placed_flows.append(placed_flow)
    chemins.append(worst_fit_path(placed_flow, available_graph))

    # On affiche le placement
    flow_view = []
    servers_view = []
    for func in placed_flow.nodes(data=True):
        flow_view.append(func[0])
        servers_view.append(func[1]['place'])
    print('Functions : ', flow_view)
    print('Servers : ', servers_view)

    physical_flow = nx.Graph()
    physical_flow.add_nodes_from(servers_view)
    for x, y in zip(servers_view[:-1], servers_view[1:]):
        # à remplacer par le path
        physical_flow.add_edge(x, y)

    placed_physical_flows.append(physical_flow)

    save_graph(available_graph, flow_name + ' placé sur le Graphe Physique',
               fig_chemin, bwd=True, cpu=True, flow=physical_flow)


save_graph(available_graph, 'Graphe Physique Complet', fig_chemin,
           bwd=True, cpu=True, flow=placed_physical_flows)

###########################################
# Approche avec les arbres de Steiner
# Étape 0

# On distingue les chaines indépendantes et les dépendantes.
common_nodes = get_common_nodes(flows)
independant_flow = [flow for flow_id, flow in enumerate(
    flows) if len(common_nodes[flow_id]) == 0]
dependant_flow = [flow for flow_id, flow in enumerate(
    flows) if len(common_nodes[flow_id]) > 0]


# On initialise le graph physique disponible
available_graph = copy.deepcopy(physical_graph)
placed_flows = []
placed_physical_flows = []

# Étape 1

# On place les chaines dépendantes

for flow in dependant_flow:

    # Variables pour les figures
    flow_id = flows.index(flow)+1
    fig_chemin = 'fig/Steiner/Dependant/'
    flow_name = 'Flow {}'.format(flow_id)
    print('\n'+flow_name)

    # On travaille sur un sous graphe en bwd:
    bwd = get_bwd(flow)
    graph_bwd = bwd_sous_graph(available_graph, bwd)

    # Rechercher un arbre de Steiner avec les noeuds communs de la chaine avec les chaines déjà placées
    # Si c'est la première chaine -> on la place librement (T = [])
    # Pour les suivantes on regarde les fonctions déjà déployées: (T=[noeud en commun avec les précédents])
    virtual_terminal_nodes = dependance(flow, placed_flows)

    placed_funcs = placed_functions(available_graph)
    physical_terminal_nodes = [placed_funcs[node]
                               for node in virtual_terminal_nodes]

    print('vT = ', virtual_terminal_nodes)
    print('pT = ', physical_terminal_nodes)

    # Steiner tree minimisant la bandwidth utilisée donc le nombre d'arrête -> weight=None
    steiner_tree = nxa.steinertree.steiner_tree(
        graph_bwd, physical_terminal_nodes, weight=None)

    if len(list(steiner_tree)) > 0:  # Si on a au moins 1 node dans le graphe (sinon erreur...)
        save_graph(steiner_tree, flow_name + ' Steiner Tree', fig_chemin)

    # Maintenant qu'on a le steiner on place ce qu'on peut:
    if len(list(steiner_tree)) >= 3:  # Si on a au moins 3 éléments: deux terminaux et un noeud à utiliser
        index_mini = list(flow).index(virtual_terminal_nodes[0])
        index_maxi = list(flow).index(virtual_terminal_nodes[-1])
        # node_between_terminal représente les func virtuelles que l'on pourrait placer sur l'arbre de Steiner
        node_between_terminal = [node for node in list(
            flow)[index_mini+1:index_maxi] if node not in virtual_terminal_nodes]
        # server_between_terminal représente les serveurs utilisable pour déployer les funcs
        server_between_terminal = [server for server in list(
            steiner_tree) if server not in physical_terminal_nodes]

    placed_flow = best_fit_nodes(flow, available_graph)
    placed_flows.append(placed_flow)

    # On affiche le placement
    flow_view = []
    servers_view = []
    for func in placed_flow.nodes(data=True):
        flow_view.append(func[0])
        servers_view.append(func[1]['place'])
    print('Functions : ', flow_view)
    print('Servers : ', servers_view)

    physical_flow = nx.Graph()
    physical_flow.add_nodes_from(servers_view)
    for x, y in zip(servers_view[:-1], servers_view[1:]):
        # à remplacer par le path
        physical_flow.add_edge(x, y)

    placed_physical_flows.append(physical_flow)

    save_graph(available_graph, flow_name + ' placé sur le Graphe Physique',
               fig_chemin, bwd=True, cpu=True, flow=physical_flow)

# Étape 2

# On place les chaines indépendantes
# On place les fonctions sur les serveurs par best fit
# c'est la même chose que lors de l'approche sans Steiner Tree

for flow in independant_flow:
    # Variables pour les figures
    flow_id = flows.index(flow)+1
    fig_chemin = 'fig/Steiner/Independant/'
    flow_name = 'Flow {}'.format(flow_id)
    print('\n'+flow_name)

    placed_flow = best_fit_nodes(flow, available_graph)
    placed_flows.append(placed_flow)

    # On affiche le placement
    flow_view = []
    servers_view = []
    for func in placed_flow.nodes(data=True):
        flow_view.append(func[0])
        servers_view.append(func[1]['place'])
    print('Functions : ', flow_view)
    print('Servers : ', servers_view)

    physical_flow = nx.Graph()
    physical_flow.add_nodes_from(servers_view)
    for x, y in zip(servers_view[:-1], servers_view[1:]):
        # à remplacer par le path
        physical_flow.add_edge(x, y)

    placed_physical_flows.append(physical_flow)

    save_graph(available_graph, flow_name + ' placé sur le Graphe Physique',
               fig_chemin, bwd=True, cpu=True, flow=physical_flow)


save_graph(available_graph, 'Graphe Physique Complet', fig_chemin,
           bwd=True, cpu=True, flow=placed_physical_flows)
