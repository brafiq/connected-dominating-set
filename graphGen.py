
import numpy as np
import random

# script for generating graphs containing N vertices

def generate_graph(N, filename):
    #print output to some location
    

    f = open(filename, "w")
    f.write(str(N) + "\n")

    #pick a vertex between 0 to N-1
    v1 = np.random.randint(0,N)
    seen = []
    seen.append(v1)
    
    # 2D adjacency list of edges
    graph = [[0 for i in range(N)] for j in range(N)]
    
    # for n-1 iterations:
    #while every vertex does not have an edge
    while len(seen) != N:
        #change for more edges

        pick = np.random.uniform(0,1)
        i = np.random.choice(seen)

        # take a vertex we've seen and connect to a new vertex, j
        if pick <= 0.5 or len(seen) <= 5:

            #print(seen)
            
            j = np.random.randint(0,N)
            while j in seen:
                j = np.random.randint(0,N)
            # print(seen)
            # print(j)
            seen.append(j)

                       
        # take a vertex we've seen and connect it to a vertex j that we've seen but i and j are not already connected
        else:

            j = np.random.choice(seen)
            while i == j or (graph[i][j] != 0 or graph[j][i] != 0):
                #print(i, j)
                i = np.random.choice(seen)
                j = np.random.choice(seen)                
        
        randVal = round(np.random.uniform(0.001,100), 3)
        graph[i][j] = randVal
        graph[j][i] = randVal
    
        #print(graph)
        #print(str(i) + " " + str(j) + " " + str(graph[i][j]))
        f.write(str(i) + " " + str(j) + " " + str(graph[i][j]) + "\n")
    
    f.close()

if __name__ == "__main__":
    
    generate_graph(25, "25.in")
    generate_graph(50, "50.in")
    generate_graph(100, "100.in")