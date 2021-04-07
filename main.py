## Dependencies

import networkx as nx
from networkx.algorithms import approximation as nxa
import random as rd
import time
import os
import shutil

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

## Graphe Physique
nb_server = rd.randint(10, 20)
# nombre max de lien = n(n-1)/2
min_link = rd.randint(nb_server-1, int(nb_server*(nb_server-1)/4))
range_cpu = (5, 10)
range_bandwidth = (7, 15)

physical_graph = graph_generation.random_connex_graph(
    nb_server, min_link, range_cpu, range_bandwidth)

# Affichage
save_graph(physical_graph, 'Graphe Physique')


## Graphe Virtuel

# v de vrange est pour virtuel (pour pas mélanger)
vrange_flow = (3, 3)
vrange_node = (4, 7)
vrange_cpu = (1, 5)
vrange_bandwidth = (5, 10)

(global_graph, flows) = graph_generation.generate_request(
    vrange_flow, vrange_node, vrange_cpu, vrange_bandwidth)

# On trie les chaines par bwd décroissante
flows = flow_sort(flows)

# Affichage des flows un par un et de la requête
for i, f in enumerate(flows):
    name = 'Flow {} '.format(i+1)
    print(name, list(f))
    save_graph(f, name, 'fig/Virtual_Graph/')
if len(flows) > 1:
    save_graph(global_graph, 'Graphe Virtuel', 'fig/Virtual_Graph/')

#################################
# Implémentation du Pseudo-Code #
#################################

## Étape 0


# On distingue les chaines indépendantes et les dépendantes.
common_nodes = get_common_nodes(flows)
independant_flow = [flow for flow_id, flow in enumerate(
    flows) if len(common_nodes[flow_id]) == 0]
dependant_flow = [flow for flow_id, flow in enumerate(
    flows) if len(common_nodes[flow_id]) > 0]
# On initialise le graph physique disponnible
available_graph = nx.Graph.copy(physical_graph)

## Étape 1

# On place les chaines indépendantes -> inverser étape 1 et 2 non ?
# On place les fonctions sur les serveurs par best fit

indep_placed_flows = []
for flow in independant_flow :
    # Variables pour les figures
    flow_id = independant_flow.index(flow)+1
    fig_chemin = 'fig/Independant_flow/flow_{}/'.format(flow_id)
    flow_name = 'Flow {}'.format(flow_id)
    print('\n'+flow_name)

    # On travaille sur un sous graphe en bwd:
    bwd = get_bwd(flow)
    graph_bwd = bwd_sous_graph(available_graph, bwd)
    save_graph(graph_bwd, flow_name + ' Graphe Physique réduit par bwd = {}'.format(bwd), fig_chemin)

    placed_flow = best_fit_nodes(flow, available_graph)
    indep_placed_flows.append(placed_flow)


## Étape 2

# On place les chaines dépendantes

placed_flows = []

for flow in dependant_flow:

    # Variables pour les figures
    flow_id = flows.index(flow)+1
    fig_chemin = 'fig/Dependant_flow/flow_{}/'.format(flow_id)
    flow_name = 'Flow {}'.format(flow_id)
    print('\n'+flow_name)

    # On travaille sur un sous graphe en bwd:
    bwd = get_bwd(flow)
    graph_bwd = bwd_sous_graph(available_graph, bwd)
    save_graph(graph_bwd, flow_name +
               ' Graphe Physique réduit par bwd = {}'.format(bwd), fig_chemin)

    # Rechercher un arbre de Steiner avec les noeuds communs de la chaine avec les chaines déjà placées
    # Si c'est la première chaine -> on la place librement (T = [])
    # Pour les suivantes on regarde les fonctions déjà déployées: (T=[noeud en commun avec les précédents])
    virtual_terminal_nodes = dependance(flow, placed_flows)
    print('T = ', virtual_terminal_nodes)

    # Il faudra prendre à terme les serveurs physiques sur lesquels seront placés les virtual_terminal_nodes
    # physical_terminal_nodes =

    # Steiner tree minimisant la bandwidth utilisée donc le nombre d'arrête -> weight=None
    steiner_tree = nxa.steinertree.steiner_tree(
        graph_bwd, virtual_terminal_nodes, weight=None)

    if len(list(steiner_tree)) > 0:  # Si on a au moins 1 node dans le graphe (sinon erreur...)
        save_graph(steiner_tree, flow_name + ' Steiner Tree', fig_chemin)

    placed_flows.append(flow)

