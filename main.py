# Dependencies

import networkx as nx
from networkx.algorithms import approximation as nxa
import random as rd
import matplotlib.pyplot as plt
import time
import os
import shutil

import graph_generation
from utils import *

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
save_graph(physical_graph, 'Graphe Physique')


# Graphe Virtuel

# v de vrange est pour virtuel (pour pas mélanger)
vrange_flow = (1, 3)
vrange_node = (4, 7)
vrange_cpu = (1, 5)
vrange_bandwidth = (5, 10)

(global_graph, flows) = graph_generation.generate_request(
    vrange_flow, vrange_node, vrange_cpu, vrange_bandwidth)

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

# Étape 0

# On trie les chaines par bwd décroissante
flows = flow_sort(flows)
# On distingue les chaines indépendantes et les dépendantes.
common_nodes = get_common_nodes(flows)


# Étape 1

# On place les chaines indépendantes -> inverser étape 1 et 2 non ?
# On place simplement avec best fit, pas de problème
# Attention bien mettre à jour le réseau physique

# Étape 2

# On place les chaines dépendantes
dependant_flow = [flow for flow_id, flow in enumerate(
    flows) if len(common_nodes[i]) > 0]

placed_flows = []

for flow in dependant_flow:
    # On travaille sur un sous graphe en bwd:
    bwd = get_bwd(flow)
    graph_bwd = bwd_sous_graph(physical_graph, bwd)
    save_graph(graph_bwd, 'Graphe Physique réduit par bwd',
               'fig/Dependant_flow/flow_{}/'.format(flows.index(flow)+1))

    # Rechercher un arbre de Steiner avec les noeuds communs de la chaine avec les chaines déjà placées
    # Si c'est la première chaine -> on la place librement (T = [])
    # Pour les suivantes on regarde les fonctions déjà déployées: (T=[noeud en commun avec les précédents])
    virtual_terminal_nodes = dependance(flow, placed_flows)
    print('T = ', virtual_terminal_nodes)

    # Il faudra prendre à terme les serveurs physiques sur lesquels seront placés les virtual_terminal_nodes
    steiner_tree = nxa.steinertree.steiner_tree(
        graph_bwd, virtual_terminal_nodes, weight='bandwidth')

    poids_arbre = 0
    for edge in steiner_tree.edges(data=True):
        poids_arbre += edge[2]['bandwidth']

    print("Poids de l'arbre: ", poids_arbre)

    if len(list(steiner_tree)) > 0:  # Si on a au moins 1 node dans le graphe (graphe non vide...)
        #plot_graph(steiner_tree, 'Steiner Tree')
        save_graph(steiner_tree, 'Steiner Tree',
                   'fig/Dependant_flow/flow_{}/'.format(flows.index(flow)+1))

    placed_flows.append(flow)
