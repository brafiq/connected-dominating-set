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

    # base case for Kn graphs
    G_copy = G.copy()
    nds = G.nodes()
    for node in nds:
        degree = np.sum([1 for i in G.neighbors(node) if i != node])
        print(len(nds))
        print(degree)
        if degree == len(nds)-1:
            # print(nds, G_copy.degree(node))
            print("SHOULD NOT GO HERE")
            dct = G.neighbors(node)
            for i in dct:
                if i != node:
                    G_copy.remove_node(i)
            print("IT GOT HERE!")
            return G_copy

    # form MST T, given G
    T = nx.minimum_spanning_tree(G)
    #T = G
            

    nodez = T.copy().nodes()
    Q = PriorityQueue()
    for n in nodez:
        Q.put((T.degree(n), n))
    
    T_copy = T.copy()
    T_prime = T.copy()

    while Q.qsize() != 0:
        #p = np.random.random()
        #if p < 0.8:
        #    v = Q.get(-1)[1]
        #else:
        v = Q.get()[1]
        # print(v)
        # print("Degree:", T.degree(v))
        # print(Q.qsize())
        if v in T_prime:
            T_prime_copy = T_prime.copy()
            T_prime.remove_node(v)
            #p = np.random.random()
        
            # heuristic 1: only remove vertices where resulting network is valid
            if (len(T_prime.nodes()) > 0 and is_valid_network(G, T_prime) and 

                # heuristic 2: only remove verties whose removal reduces average pairwise distance
                average_pairwise_distance(T_prime) < average_pairwise_distance(T_copy)):
    
                    if len(T_copy.nodes()) > 0:
                        T_copy.remove_node(v)

                        # heuristic 3: add nodes with larger degrees first to the queue 
                            # or could add smaller degree ones first) but larger degrees seems to perform better
                        # el = {}
                        # for node in T_copy.nodes():
                        #     el[node] = T_copy.degree(node)
                        
                        # # sort nodes based on degree
                        # el = dict(sorted(el.items(), key=lambda x: x[1], reverse=True))
                    
                        # for i in el.items():
                        #     Q.append(i[0])
                        for node in T_copy.nodes():
                            Q.put((T_copy.degree(node), node))
                        # print("****** Added new Nodes *******")
                    
                    else:
                        T_prime = T_prime_copy
            else:
                T_prime = T_prime_copy
                
    return T_copy
        

if __name__ == '__main__':

    path = "./inputs/small-4.in"
    G = read_input_file(path)
    M = nx.minimum_spanning_tree(G)
    T = solve(G)

    assert is_valid_network(G, T)
    print("Average pairwise distance of MST: {}".format(average_pairwise_distance(M)))
    print("Average pairwise distance of T: {}".format(average_pairwise_distance(T)))

    # print("*********START***********")
    # # vals = {"small-": 304, "medium-": 304, "large-": 400}
    # vals = {"small-": 15, "medium-": 15, "large-": 15}
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

