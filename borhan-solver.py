import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import matplotlib.pyplot as plt
import sys
import numpy as np
import random


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # base case for Kn graphs
    G_copy = G.copy()
    nds = G.nodes()
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
            return G_copy

    # form MST T, given G
    T = nx.minimum_spanning_tree(G)

    nodez = T.copy().nodes()
    Q = []

    for n in nodez:
        stuff = (n, T.degree(n))
        Q.append(stuff)
    T_copy = T.copy()
    T_prime = T.copy()

    # print(Q)

    while Q:

        Q = sorted(Q, key=lambda x: x[1], reverse=False)

        # print(Q)

        v = Q.pop(0)[0]
        # print("DEGREE: ", v)
    
        if v in T_prime:
            T_prime_copy = T_prime.copy()
            T_prime.remove_node(v)
            p = np.random.random()
        
            # heuristic 1: only remove vertices where resulting network is valid
            if (len(T_prime.nodes()) > 0 and is_valid_network(G, T_prime) and 

                # heuristic 2: only remove verties whose removal reduces average pairwise distance
                average_pairwise_distance(T_prime) < average_pairwise_distance(T_copy)):
    
                    if len(T_copy.nodes()) > 0:
                        T_copy.remove_node(v)

                        for node in T_copy.nodes():
                            stuff = (node, T_copy.degree(node))
                            Q.append(stuff)
            else:
                T_prime = T_prime_copy
                    
        
    # For each vertex: --> USE HEURISTIC FOR THIS!
        #Check if remove the vertex is_a_valid_networK:
            #If it is a valid network:
                #Remove the vertex and calculate the average pairwise distance
                    #If the averagepairwise distance is higher:
                        #ignroe that vertex
                    #If the avergepairwise distance is lower:
                        #remove vertex
    # print(len(T_copy))
    return T_copy

if __name__ == '__main__':

    print("*********START***********")

    path = "./inputs/small-4.in"       
    G = read_input_file(path)
    M = nx.minimum_spanning_tree(G)
    T = solve(G)

    ####### plotting the graph #######
    # plt.figure(figsize = (20, 20))
    # plt.subplot(121)
    # edges = nx.get_edge_attributes(T, 'weight')
    # nx.draw_networkx(T, with_labels=True, edge_labels=edges)
    # plt.show()
    ##################################

    assert is_valid_network(G, T)
    print("Average pairwise distance of MST: {}".format(average_pairwise_distance(M)))
    print("Average pairwise distance of T: {}".format(average_pairwise_distance(T)))
    print()
    # write_output_file(T, './outputs/' + item[0] + str(i) + '.out')
    print("*********DONE***********")


    # print("*********START***********")
    # vals = {"small-": 304, "medium-": 304, "large-": 401}
    # #vals = {"small-": 15, "medium-": 15, "large-": 15}
    # # vals = {"large-": 2}

    # output = 0

    # for item in vals.items():
    #     for i in range(1, item[1]):
    #         path = "./inputs/" + item[0] + str(i) + ".in"       
    #         G = read_input_file(path)
    #         M = nx.minimum_spanning_tree(G)
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
    #         print("Finishing ", item[0] + str(i))
    #         # print()
    #         # write_output_file(T, './outputs/' + item[0] + str(i) + '.out')
    # print("*********DONE***********")
    # print()
    # print("FINAL OUTPUT:", output)

