from graph import WeightedDiGraph, create_random_weighted_graph
from AllPairs import PriorityQueue
import timeit 
import matplotlib.pyplot as plt
import random
import numpy as np

##Normal dijkstras 
def dijkstrasNORMAL(G: WeightedDiGraph, source: int):
    minHeap = PriorityQueue()
    distTo = {node: float('inf') for node in (G.graph)}
    parentEdge = {node: -1 for node in (G.graph)}
    distTo[source] = 0
    parentEdge[source] = source

    minHeap.push(source, 0)

    while not minHeap.is_empty():
        curr_node, curr_dist = minHeap.pop()

        for neighbourgh in G.graph[curr_node]:
            new_dist = curr_dist + G.weight[(curr_node, neighbourgh)]
            if new_dist < distTo[neighbourgh]:
                distTo[neighbourgh] = new_dist
                parentEdge[neighbourgh] = curr_node
                minHeap.push(neighbourgh,new_dist)

    return distTo


##Modified dijkstras 
def dijkstras_2(G: WeightedDiGraph, source: int, k:int):
    ##Init our dictionaries
    minHeap = PriorityQueue()
    distTo = {node: float('inf') for node in (G.graph)}
    parentEdge = {node: -1 for node in (G.graph)}
    distTo[source] = 0
    parentEdge[source] = source

    ##This will make sure that none of our nodes go above k relaxes
    numRelaxes = {node: 0 for node in (G.graph)}


    minHeap.push(source, 0)

    ##Regular dijkstras 
    while not minHeap.is_empty():
        curr_node, curr_dist = minHeap.pop()

        ##Loop through neighbours and relax that edge
        for neighbourgh in G.graph[curr_node]:
            ##If we have already relaxed k times, move on 
            if numRelaxes[neighbourgh] >= k:
                continue

            ##Edge relaxation 
            new_dist = curr_dist + G.weight[(curr_node, neighbourgh)]
            if new_dist < distTo[neighbourgh]:
                distTo[neighbourgh] = new_dist
                parentEdge[neighbourgh] = curr_node
                minHeap.push(neighbourgh,new_dist)
                numRelaxes[neighbourgh] += 1
    
    ##Trace the paths backwords
    paths = {}
    for key in parentEdge.keys():
        paths[key] = reconstruct_path(parentEdge,source,key)
    return [distTo,paths]

def bellman_ford(G: WeightedDiGraph, source: int, k: int):
    ##Init dictionaries
    distance = {node: float('inf') for node in G.graph}
    distance[source] = 0
    parent = {node: -1 for node in G.graph}
    parent[source] = source
    ##Dict to check number of relaxes
    numRelaxes = {node: 0 for node in (G.graph)}

    ##Normal bellman_ford
    # Performing at most n - 1 edge relaxations
    for _ in range (len(G.graph)):
        for (u,v),weight in G.weight.items():
            ##If we have relaxed v k times already, skip over
            if numRelaxes[v] >= k:
                continue
            ##Relax edge
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                parent[v] = u
                numRelaxes[v] += 1
    
    ##Detect for negative cycles
    for (u,v),weight in G.weight.items():
        ##We need to make sure that the new update isn't just because of our k paramater
        if numRelaxes[v] >= k:
                continue
        if distance[u] + weight < distance[v]:
            print("Negative cycle detected")
            return 
    ##Trace the paths backwords
    paths = {}
    for key in parent.keys():
        paths[key] = reconstruct_path(parent,source,key)

    return [distance,paths]

def reconstruct_path(came_from, source, destination):
    # Add the end of the path since we will work our way backwards.
    path = [destination]
    # This will track where we currently are in the path. 
    current = destination
    while current != source: 
        # To prevent an infinite loop we check if the current element we are looking for is in the dictionary.
        if current not in came_from: 
            return []
        # Move on to the next element in the path.
        current = came_from[current]
        # Add the current element to the path. 
        path.append(current)
    # We have to reverse the list in the end since we are adding elements in reverse order.
    return path[::-1]

def varyingDensities():
    ##Trials
    N = 100

    ##Array inits
    dijTimes = []
    bellTimes = []

    ##For plot funciton
    xAxis = []

    ##Various densities
    densities = [(7,15),(7,18),(7,21),(7,24),(7,27),(7,30)]

    for graph in densities:

        ##Get the information we need
        xAxis.append(str(graph))
        numNodes = graph[0]
        numEdges = graph[1]
        dijkstras = 0
        bellman = 0
        
        ##Run experiment N times
        for _ in range (N):
            #Create random weighted grpah and get rando mstart node
            g = create_random_weighted_graph(numNodes,numEdges,100,0)
            source = random.randint(0,6)

            ##Dijkstras
            start = timeit.default_timer()
            dijkstras_2(g,source,6)
            stop = timeit.default_timer()
            dijkstras += (stop - start) * (10**6)

            ##Bellman
            start = timeit.default_timer()
            bellman_ford(g,source,6)
            stop = timeit.default_timer()
            bellman += (stop - start) * (10**6)

        dijTimes.append(dijkstras / N)
        bellTimes.append(bellman / N )

    ##Plot 
    densities_plot(xAxis, dijTimes, "Dijkstras on varying densities")
    densities_plot(xAxis, bellTimes, "Bellman-Ford on varying densities")
    

def varyingKValues():
    ##Trials
    N = 100

    ##Array inits
    dijAcc = []
    bellAcc = []

    ##For plot funciton
    xAxis = []

    ##Various K values
    kValues = [1,2,3,4,5,6]

    for kValue in kValues:

        ##Get the information we need
        xAxis.append(str(kValue))
        k = kValue
        dijkstrasCorrect = 0
        bellmanCorrect = 0
        
        ##Run experiment N Times
        for _ in range (N):
            #Create random weighted grpah and get rando mstart node
            g = create_random_weighted_graph(10,60,100,0)
            source = random.randint(0,6)

            ##Modified Dijkstras
            dInfo = dijkstras_2(g,source,k)
            dWeights = dInfo[0]
            
            ##Bellman
            bInfo = bellman_ford(g,source,k)
            bWeights = bInfo[0]

            ##Normal Dijkstras
            correctWeights = dijkstrasNORMAL(g,source)

            ##Check to see if the modified algorithms match the correct one
            dMatch = True
            bMatch = True
            for key in correctWeights:
                if (not dMatch and not bMatch):
                    break
                if correctWeights[key] != dWeights[key]:
                    dMatch = False
                if correctWeights[key] != bWeights[key]:
                    bMatch = False


            ##If it matched the correct, add one to the value
            if (dMatch):
                dijkstrasCorrect += 1
            if (bMatch):
                bellmanCorrect += 1

        print(dijkstrasCorrect / N,bellmanCorrect / N)
        dijAcc.append(dijkstrasCorrect / N)
        bellAcc.append(bellmanCorrect / N )

    ##Plot 
    varying_k_plot(xAxis, dijAcc, "Dijkstras accuracy on varying k values")
    varying_k_plot(xAxis, bellAcc, "Bellman-Ford accuracy on varying k values")
    
    

##Plot function for densities
def densities_plot(xLabel, run_arr, title):
    x = xLabel
    fig=plt.figure(figsize=(20,8))
    plt.bar(x,run_arr)
    ##plt.axhline(mean,color="red",linestyle="--",label="Avg")
    #plt.legend([f"Average: {mean} μs"])
    plt.xlabel("Graph with N nodes and E edges")
    plt.ylabel("Average run time for 100 trials in ms order of 1e-6")
    plt.title(title)
    plt.savefig(title)

##Plot function for k
def varying_k_plot(xLabel, run_arr, title):
    x = xLabel
    fig=plt.figure(figsize=(20,8))
    plt.bar(x,run_arr)
    #plt.axhline(mean,color="red",linestyle="--",label="Avg")
    #plt.legend([f"Average: {mean} μs"])
    plt.xlabel("100 runs of modified alogrithms with value k")
    plt.ylabel("Percent of accurate runs")
    plt.title(title)
    plt.savefig(title)


#varyingDensities()
#varyingKValues()