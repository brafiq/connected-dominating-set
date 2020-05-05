# CS 170 Project Spring 2020
# Borhan Rafiq, Ananya Krishnan, Sara Reynolds

# Files:
  - `parse.py`:   functions to read/write inputs and outputs
  - `solver.py`:  where you should be writing your code to solve inputs
  - `utils.py`:   contains functions to compute cost and validate NetworkX graphs
  - `inputs`:     contains inputs of graph 
      - small: 303
      - medium: 303
      - large: 400

  - `outputs`:    outputs of valid networks for corresponding input graph
      - small: 303
      - medium: 303
      - large: 400

# Function Overview in solver.py:

    1. generateTree(G)
    
        purpose: generate random trees that connects every node in the original graph implemented by ensuring that no added vertex creates a cycle in the graph
        inputs: G - a networkx Graph
        outputs: T - a networkx Graph that is a valid network
        
    2. remove_random(n, T, G)

        purpose: remove random edges such that we minimize the average pairwise distance and the trees stays connected
        inputs: n - the number of nodes to remove, T - a valid networkx Graph to remove nodes from, G - the original networkxGraph 
        outputs: T - a networkx Graph that is a valid network with n removed nodes
           
    3. process(G)
    
        purpose: prune nodes from the network in order of smallest degree to largest degree via a Priority Queue
        inputs: T a networkx Graph that is a vaid network, and G - the original networkx graph
        outputs: T, a networkx Graph that is a valid network
        
    4. solve(G)

        purpose: generate a number of trees based on G and the MST of G, use remove_random() to randomly prune, use process() to prune based on degrees of nodes, and return the tree with the minimum average pairwise distance
        inputs: G, a networkx Graph
        outputs: T - a networkx Graph that is a valid network

# To Run: 

  1. Run python3 -m pip install newtorkx on your terminal to install the networkx library (https://networkx.github.io/documentation/stable/install.html)
  2. Navigate into the directory with solver.py in a terminal
  3. Run python3 solver.py in the terminal