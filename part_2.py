from graph import WeightedGraph 
from AllPairs import PriorityQueue

def dijkstras(G: WeightedGraph, source: int):
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


def dijkstras_2(G: WeightedGraph, source: int, k:int):
    minHeap = PriorityQueue()
    distTo = {node: float('inf') for node in (G.graph)}
    parentEdge = {node: -1 for node in (G.graph)}
    numRelaxes = {node: 0 for node in (G.graph)}
    distTo[source] = 0
    parentEdge[source] = source

    minHeap.push(source, 0)

    while not minHeap.is_empty():
        curr_node, curr_dist = minHeap.pop()

        for neighbourgh in G.graph[curr_node]:
            if numRelaxes[neighbourgh] >= k:
                continue
            new_dist = curr_dist + G.weight[(curr_node, neighbourgh)]
            if new_dist < distTo[neighbourgh]:
                distTo[neighbourgh] = new_dist
                parentEdge[neighbourgh] = curr_node
                minHeap.push(neighbourgh,new_dist)
                numRelaxes[neighbourgh] += 1
    return distTo

def bellmanFord(G:WeightedGraph, source: int, k: int):
    distTo = {node: float('inf') for node in (G.graph)}
    parentEdge = {node: -1 for node in (G.graph)}
    onQ = {node: False for node in (G.graph)}
    queue = []
    distTo[source] = 0
    parentEdge[source] = source

    queue.append(source)
    onQ[source] = True

    while queue != []:
        pass
    return 0


def bellman_ford(G: WeightedGraph, source: int, k: int):
    distance = {node: float('inf') for node in G.graph}
    distance[source] = 0
    parent = {node: -1 for node in G.graph}
    parent[source] = source
    numRelaxes = {node: 0 for node in (G.graph)}

    # Performing at most n - 1 edge relaxations
    for _ in range (len(G.graph)):
        for (u,v),weight in G.weight.items():
            if numRelaxes[v] >= k:
                continue
            if distance[u] + weight < distance[v]:
                print(u, distance[u], v, distance[v],weight)
                distance[v] = distance[u] + weight
                print(v,distance[v])
                parent[v] = u
    
    for (u,v),weight in G.weight.items():
        if distance[u] + weight < distance[v]:
            print("Negative cycle detected")
            return 
    
    return [distance,parent]
