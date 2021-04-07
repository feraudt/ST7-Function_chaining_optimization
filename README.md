# Function chaining optimization

Graph approach for the optimization of function chaining for IoT using Steiner trees.  
School project conducted by CentraleSupélec students.

## Packages installation

We chose to use the python library [NetworkX](https://networkx.org/) for graphs and Steiner trees management.  
Install it with the following command :

    $ pip install networkx

Documentation available at :

    https://networkx.org/documentation/stable/index.html

## Organisation du projet

    main.py - Contient la structure globale
    utils.py - Contient des fonctions d'utilités pour ne pas surcharger main.py
    fit_algo.py - Contient les fonctions pour placer les chaines sur les graphes, optimisation best fit, PCC ...

    graph_generation/physical_graph - Contient les fonctions pour générer le graphe physique
    graph_generation/virtual_graph - Contient les fonctions pour générer le graphe virtuel
