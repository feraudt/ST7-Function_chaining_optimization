import networkx as nx
import random
import matplotlib.pyplot as plt

from utils import *
# Graphe Physique

server = []
nb_server = random.randint(10, 20)

for i in range(nb_server):
    capacity = random.randint(3, 10)
    server.append((i+1, {'capacity': capacity}))

link = []
# nombre max de lien = n(n-1)/2
nb_link = random.randint(nb_server, nb_server*(nb_server-1)/2)

for i in range(nb_link):
    s1 = random.randint(1, nb_server+1)
    s2 = random.randint(1, nb_server+1)
    while s2 == s1:
        s2 = random.randint(1, nb_server+1)
    bandwidth = random.randint(7, 15)

    link.append((s1, s2, {'bandwidth': bandwidth}))

physical_graph = nx.Graph()
physical_graph.add_nodes_from(server)
physical_graph.add_edges_from(link)

# On rend le graphe connexe si jamais
physical_graph = make_connex(physical_graph)

# Affichage
plt.plot()
nx.draw(physical_graph, with_labels=True)
plt.show()
