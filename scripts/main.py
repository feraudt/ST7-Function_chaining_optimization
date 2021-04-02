# Dependencies

import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import time

from utils import *

# Graphe Physique

nb_server = rd.randint(10, 20)

# nombre max de lien = n(n-1)/2
min_link = rd.randint(nb_server-1, int(nb_server*(nb_server-1)/4))

range_cpu = (5, 10)
range_bandwidth = (7, 15)

physical_graph = random_connex_graph(
    nb_server, min_link, range_cpu, range_bandwidth)

# Affichage
plot_graph(physical_graph)


# Graphe Virtuel
# v de vrange est pour virtuel (pour pas mélanger)
vrange_flow = (1, 3)
vrange_node = (4, 7)
vrange_cpu = (1, 5)
vrange_bandwidth = (5, 10)

(global_graph, flows) = generate_request(
    vrange_flow, vrange_node, vrange_cpu, vrange_bandwidth)

# Affichage des flows un par un et de la requête
for i, f in enumerate(flows):
    print('Flow {} : '.format(i+1), list(f))
    plot_graph(f)
plot_graph(global_graph)

(dependant_flow, independant_flow) = dependance(flows)
print('noeud et chaines dépendantes:', dependant_flow)
print('chaines indépendantes', independant_flow)
