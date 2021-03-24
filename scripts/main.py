## Dependencies

import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import time

from utils import *

## Graphe Physique

server = []
nb_server = rd.randint(10, 20)

for i in range(nb_server):
    capacity = rd.randint(3, 10)
    server.append((i+1, {'capacity': capacity}))

link = []
# nombre max de lien = n(n-1)/2
nb_link = rd.randint(nb_server, nb_server*(nb_server-1)/2)

for i in range(nb_link):
    s1 = rd.randint(1, nb_server+1)
    s2 = rd.randint(1, nb_server+1)
    while s2 == s1:
        s2 = rd.randint(1, nb_server+1)
    bandwidth = rd.randint(7, 15)

    link.append((s1, s2, {'bandwidth': bandwidth}))

physical_graph = nx.Graph()
physical_graph.add_nodes_from(server)
physical_graph.add_edges_from(link)


# On rend le graphe connexe si jamais
physical_graph = make_connex(physical_graph)

# Affichage
plot_graph(physical_graph)

## Graphe Virtuel

virtual_link = []
virtual_fonctions = []
# première chaine
nb_fonctions = rd.randint(4, 7)

for i in range(nb_fonctions):
    cpu = rd.randint(1, 5)
    virtual_fonctions.append((i+1, {'capacity': cpu}))

for i in range(nb_fonctions-1):
    bandwidth = rd.randint(5, 10)
    virtual_link.append((i+1, i+2, {'bandwidth': bandwidth}))

# Deuxième chaine le code est pas beau mais ça marche
nb_fonctions = rd.randint(4, 7)

for i in range(nb_fonctions):
    cpu = rd.randint(1, 5)
    # on met l'index 2 pour le deuxième élément de la chaine
    index = len(virtual_fonctions)+1 if i != 2 else 2
    virtual_fonctions.append((index, {'capacity': cpu}))

n = len(virtual_link) + 1
for i in range(nb_fonctions):
    bandwidth = rd.randint(5, 10)
    # Code pas beau qui met les bonnes valeurs pour la génération des links
    if i == 0:
        virtual_link.append((n+1, 2, {'bandwidth': bandwidth}))
    elif i == 1:
        virtual_link.append((2, n+2, {'bandwidth': bandwidth}))
    else:
        virtual_link.append((n+i, n+i+1, {'bandwidth': bandwidth}))

# Génération
virtual_graph = nx.DiGraph()
virtual_graph.add_nodes_from(virtual_fonctions)
virtual_graph.add_edges_from(virtual_link)

# Affichage
plot_graph(virtual_graph)

