# Dependencies

import networkx as nx
from networkx.algorithms import approximation as nxa
import random as rd
import matplotlib.pyplot as plt
import time

import graph_generation
from utils import *

# Graphe Physique
nb_server = rd.randint(10, 20)
# nombre max de lien = n(n-1)/2
min_link = rd.randint(nb_server-1, int(nb_server*(nb_server-1)/4))
range_cpu = (5, 10)
range_bandwidth = (7, 15)

physical_graph = graph_generation.random_connex_graph(
    nb_server, min_link, range_cpu, range_bandwidth)

# Affichage
plot_graph(physical_graph, 'Graphe Physique')


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
    plot_graph(f, name)
if len(flows) > 1:
    plot_graph(global_graph, 'Graphe Virtuel')

#################################
# Implémentation du Pseudo-Code #
#################################

# Étape 0

# On distingue les chaines indépendantes et les dépendantes.
(dependant_flow, independant_flow) = dependance(flows)
# On trie les chaines par bwd décroissante
flows = flow_sort(flows)

# Étape 1

# On place les chaines indépendantes ?? -> inverser étape 1 et 2 non ?
# Attention bien mettre à jour le réseau physique

# Étape 2

# On place les chaines dépendantes
# On travaille sur un sous graphe en bwd:
graph_bwd = bwd_sous_graph(physical_graph, 10)
# Rechercher un arbre de Steiner avec les noeuds communs des chaines ???? A quoi ça sert ?
terminal_nodes = [tup[0] for tup in dependant_flow]
steiner_tree = nxa.steinertree.steiner_tree(graph_bwd, terminal_nodes)

plot_graph(graph_bwd, 'Graphe Physique réduit par bwd')
plot_graph(steiner_tree, 'Steiner Tree')
