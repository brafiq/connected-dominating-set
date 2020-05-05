import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import matplotlib.pyplot as plt
import sys
import numpy as np
import random
from queue import PriorityQueue



def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # copy G and its nodes to use later
    nds = G.nodes()
    G_copy = G.copy()

    # remove self edges from graph
    for n in nds:
        try:
            G_copy.remove_edge(n,n)
        except:
            continue
    
    # base case for Kn graphs
    for node in nds:
        degree = np.sum([1 for i in G.neighbors(node) if i != node])
        # print(len(nds))
        # print(degree)
        if degree == len(nds)-1:
            # print(nds, G_copy.degree(node))
            # print("SHOULD NOT GO HERE")
            dct = G.neighbors(node)
            for i in dct:
                if i != node:
                    G_copy.remove_node(i)
            # print("IT GOT HERE!")
            # print(G_copy)
            # print(is_valid_network(G, G_copy))
            return G_copy

    # form MST T, given G
    T = nx.minimum_spanning_tree(G)            

    nodez = T.copy().nodes()
    Q = PriorityQueue()
    for n in nodez:
        Q.put((T.degree(n), n))
    
    #remove one node
    T_copy = T.copy() # compare against
    T_test = T.copy() # test tree - remove from here
    
    # # remove two nodes at once
    # Q_copy = Q
    # T_parr = T.copy() # compare against
    # T_test_parr = T.copy() # test tree - remove two from here

    while Q.qsize() != 0:
                    
        first_removal = Q.get()[1]
        # second_removal = None
        
        # #if option for second DO IT
        # if Q.qsize() >= 2:
        #     second_removal = Q.get()[1]

        if first_removal in T_test:

            # 2 nodes
            # if second_removal in T_test_parr and first_removal in T_test_parr:
                
            #     T_test_parr_copy = T_test.copy()
            #     T_test_parr.remove_node(first_removal)
            #     T_test_parr.remove_node(second_removal)
            #     if (len(T_test.nodes()) > 0 and is_valid_network(G, T_test):
            
            T_test_copy = T_test.copy()
            T_test.remove_node(first_removal)
        
            # heuristic 1: only remove vertices where resulting network is valid
            if (len(T_test.nodes()) > 0 and is_valid_network(G, T_test) and 

                # heuristic 2: only remove verties whose removal reduces average pairwise distance
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

    path = "./inputs/large-114.in"       
    G = read_input_file(path)
    M = nx.minimum_spanning_tree(G)
    T = solve(G)

    ####### plotting the graph #######
    # plt.figure(figsize = (20, 20))
    # plt.subplot(121)
    # edges = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx(G, with_labels=True, edge_labels=edges)
    # plt.show()
    ##################################

    assert is_valid_network(G, T)
    print("Average pairwise distance of MST: {}".format(average_pairwise_distance(M)))
    print("Average pairwise distance of T: {}".format(average_pairwise_distance(T)))
    print()
    # write_output_file(T, "./outputs/large-400.out")
    print("*********DONE***********")

    # print("*********START***********")
    # # vals = {"small-": 304, "medium-": 304, "large-": 401}
    # # vals = {"small-": 16, "medium-": 16, "large-": 16}
    # vals = {"large-": 2}
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
    #         print("Finished", item[0]+str(i) + ":", average_pairwise_distance(T))
    #         # print()
    #         # write_output_file(T, './outputs/' + item[0] + str(i) + '.out')
    # print("FINAL OUTPUT:", output)
    # print("*********DONE***********")
