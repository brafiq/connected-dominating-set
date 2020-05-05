import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import matplotlib.pyplot as plt
import sys
import numpy as np
import random
from queue import PriorityQueue


def generateTree(G):
    edges = []
    for line in nx.generate_edgelist(G,data=['weight']):
        vals = line.split(" ")
        if len(vals) == 3:
            edges.append((int(vals[0]), int(vals[1]), float(vals[2])))        

    new_Graph = nx.Graph()

    for i in G.nodes():
        new_Graph.add_node(i)

    G_edges = edges
    
    
    while not nx.is_tree(new_Graph) and not is_valid_network(G, new_Graph): #nx.number_connected_components(new_Graph) != 1: 
        n = np.random.choice(range(len(G_edges)))
        edgeVal = G_edges[n]
        new_Graph.add_edge(edgeVal[0], edgeVal[1], weight=edgeVal[2])
        has_cycle = True
        try: 
            nx.find_cycle(new_Graph)
        except: 
            has_cycle = False
            
        if has_cycle == True:
            new_Graph.remove_edge(edgeVal[0], edgeVal[1])
        else:
            G_edges.remove(edgeVal)

    assert nx.is_tree(new_Graph)
    assert is_valid_network(G, new_Graph)

    return new_Graph

def solve(G):

    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    # for testing small-6
    # if len(G.nodes()) <= 5:
    #     G_copy = G.copy()
    #     G_copy.remove_node(4)
    #     G_copy.remove_node(3)
    #     return G_copy

    G_copy = G.copy() 
    nds = G.nodes()

    #remove self edges 
    for n in nds:
        try:
            G_copy.remove_edge(n,n)
        except:
            continue
    
    # base case for Kn graphs
    for node in nds:
        degree = np.sum([1 for i in G.neighbors(node) if i != node])

        if degree == len(nds)-1:
    
            dct = G.neighbors(node)
            for i in dct:
                if i != node:
                    G_copy.remove_node(i)

            return G_copy
    
    #get MST of G
    T = nx.minimum_spanning_tree(G) 
    T1 = generateTree(G)

    #generate X trees from MST of G

    smallOptimization = False
    if len(G.nodes()) <= 25:
        smallOptimization = True
    if smallOptimization:
        X = 5
        max_trees = 100
    else:
        # X = 5
        X = 1
        max_trees = 1

    trees = []

    trees.append(nx.minimum_spanning_tree(G))

    #count = 0
    nums = []
        
    for i in range(1, round(len(T.nodes()))):
        nums.append(i)
    
    for _ in range(X):
        # print("Entering iteration")

        #MST adapted
        print(nums)
        # print(len(nums), np.random.choice(nums))
        for i in range(max_trees):
            for j in nums:
                if j > 65:
                    trees.append(remove_random(np.random.choice(j), T.copy(), G))
    
        # for i in range(40):
        #     trees.append(remove_pq(np.random.choice(nums), T.copy(), G, 1))
        #     trees.append(remove_pq(np.random.choice(nums), T.copy(), G, -1))

        # for i in range(max_trees):
        #     trees.append(remove_random(np.random.choice(nums), generateTree(G), G))
        
        # trees.append(remove_pq(np.random.choice(nums), T1.copy(), G, 1))
        #MST Tree

        # print("Finishing iteration")
    
    minimum = float("inf")
    minimum_tree = None
    i = 0

    # print(trees)

    for t in trees:
        # print(is_valid_network(G, t), i)

        solver = process(t, G)
        # print(is_valid_network(G, solver), i)
        mini = average_pairwise_distance(solver)
        # mini = average_pairwise_distance(t)
        print(i, mini)
        if mini < minimum :
            # print("In here!")
            minimum = mini
            # print("val", minimum)
            minimum_tree = solver
            # minimum_tree = t
        i+=1
    return minimum_tree
    
def remove_random(n, T, G):
    """ Remove n nodes at random from T """
    nodes = T.nodes()
    #print(nodes)
    to_remove = np.random.choice(nodes, n)
    # print(to_remove)
    T_copy = T.copy()
    for x in to_remove:
        if x in T_copy:
            T_copy.remove_node(x)
    #count = 0 
    
    def find_tree(n, T_copy, G):

        if n == 0:
            return T.copy()

        iters = 0

        # print(n, len(T_copy.nodes()))

        while not (is_valid_network(G, T_copy)):
            if iters >= 20:
                T_copy = T.copy()
                break
            T_copy = T.copy()
            # print(len(T_copy.nodes()), len(T.nodes()))
            to_remove = np.random.choice(T_copy.nodes(), n, replace=False)
            for x in to_remove:
                T_copy.remove_node(x)
            #count += 1
            iters += 1
        
        if not is_valid_network(G, T_copy):
            
            return find_tree(n - 1, T_copy, G)
    
        return T_copy
        
    return find_tree(n, T_copy, G)

def remove_pq(n, T, G, deg=1):
    """Remove n vertices based on priority queue.
    If deg = 1 remove lowest degree vertices first. 
    If deg = -1 remove highest degree vertices first. """
    nodez = T.nodes()
    T_copy = T.copy()
    Q = PriorityQueue()
    for n in nodez:
        Q.put((deg*T.degree(n), n))
    num_i = n 
    count = 0
    while (num_i != 0) or (Q.qsize() != 0):
        if Q.qsize() == 0:
            break
        count += 1
        v = Q.get()[1]
        T_og = T_copy.copy()
        T_copy.remove_node(v)
        if not is_valid_network(G, T_copy): 
            T_copy = T_og
        else:
            num_i -= 1
    return T_copy


def process(T, G):
    """
    Args:
        T: networkx.Graph
        G: original networkx.Graph

    Returns:
        T: networkx.Graph
    """
  
    nodez = T.copy().nodes()
    Q = PriorityQueue()
    for n in nodez:
        Q.put((T.degree(n), n))
    
    #remove one node
    T_copy = T.copy() # compare against
    T_test = T.copy() # test tree - remove from here
    
    # # remove two nodes at once
    
    while Q.qsize() != 0:
                    
        first_removal = Q.get()[1]
        # second_removal = None
        
        # #if option for second DO IT
        # if Q.qsize() >= 2:
        #     second_removal = Q.get()[1]

        if first_removal in T_test:
            
            T_test_copy = T_test.copy()
            T_test.remove_node(first_removal)
        
            # heuristic 1: only remove vertices where resulting network is valid
            if (len(T_test.nodes()) > 0 and is_valid_network(G, T_test) and 

                # heuristic 2: only remove vertices whose removal reduces average pairwise distance
                average_pairwise_distance(T_test) < average_pairwise_distance(T_copy)):
    
                    
                    if len(T_copy.nodes()) > 0:
                        #neighs = T_copy.neighbors(v)
                        T_copy.remove_node(first_removal)
                        # if w and w in T_copy:
                        #     T_copy.remove_node(w)
                        #T_copy.remove_node(w)

                        # for node in T_copy.nodes():
                        #     # print("ADDED:", node)
                        #     Q.put((T_copy.degree(node), node))

                        Q = PriorityQueue()
                        for node in T_copy.nodes():
                            Q.put((T_copy.degree(node), node))

                    else:
                        T_test = T_test_copy
            else:
                T_test = T_test_copy
    
    return T_copy
        

if __name__ == '__main__':

    print("*********START***********")

    path = "./inputs/large-362.in"       
    G = read_input_file(path)
    M = nx.minimum_spanning_tree(G)
    T = solve(G)

    # ####### plotting the graph #######
    # plt.figure(figsize = (20, 20))
    # plt.subplot(121)
    # edges = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx(G, with_labels=True, edge_labels=edges)
    # plt.show()
    # ##################################

    assert is_valid_network(G, T)
    print("Average pairwise distance of MST: {}".format(average_pairwise_distance(M)))
    print("Average pairwise distance of T: {}".format(average_pairwise_distance(T)))
    print()
    # write_output_file(T, "./outputs/large-400.out")
    print("*********DONE***********")

    # print("*********START***********")
    # vals = {"small-": 304, "medium-": 304, "large-": 401}
    # # vals = {"small-": 6}
    # output = 0
    # for item in vals.items():
    #     for i in range(1, item[1]):
    #         path = "./inputs/" + item[0] + str(i) + ".in"       
    #         G = read_input_file(path)
    #         # M = nx.minimum_spanning_tree(G)
    #         T = solve(G)

    #         ####### plotting the graph #######
    #         # plt.figure(figsize = (20, 20))
    #         # plt.subplot(121)
    #         # edges = nx.get_edge_attributes(G, 'weight')
    #         # nx.draw_networkx(G, with_labels=True, edge_labels=edges)
    #         # plt.show()
    #         ##################################

    #         assert is_valid_network(G, T)
    #         # print("Average pairwise distance of MST: {}".format(average_pairwise_distance(M)))
    #         # print("Average pairwise distance of T: {}".format(average_pairwise_distance(T)))
    #         output += average_pairwise_distance(T)
    #         # print("Finished ", item[0], str(i))
    #         print("Finished", item[0]+str(i) + ":", average_pairwise_distance(T))
    #         # print()
    #         write_output_file(T, './outputs/' + item[0] + str(i) + '.out')
    # print("FINAL OUTPUT:", output)
    # print("*********DONE***********")
