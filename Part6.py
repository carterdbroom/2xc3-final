from AllPairs import PriorityQueue
from typing import List, Dict
import AStar as A

class Graph():
    def __init__(self, nodes):
        self.graph = {}
        for i in range(nodes):
            self.graph[i] = []

    def get_adj_nodes(self, node: int) -> List[int]:
        ##Get adjacency list
        return self.graph[node]

    def add_node(self):
        #add a new node number = length of existing node
        self.graph[len(self.graph)] = []

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph[node2]:
            self.graph[node1].append(node2)
    
    def get_num_of_nodes(self) -> int:
        len(self.graph)

    ##I don't know what this function was supposed to be
    def w(self,node: int) -> float:
        return 69.0


class WeightedGraph(Graph):
    def __init__(self):
        super().__init__()
        self.weight = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph[node2]:
            self.graph[node1].append(node2)
            self.weight[(node1, node2)] = weight

class HeuristicGraph(WeightedGraph):
    def __init__(self):
        ## You can't make private attributes in python T_T
        self.heuristic = {}

    def get_heuristic(self) -> Dict[int,float]:
        return self.heuristic
    

class SPAlgorithm():
    def calc_sp(graph: Graph, source: int, dest: int) -> float : 
        pass


class Dijkstra(SPAlgorithm):
    def calc_sp(self, graph: WeightedGraph, source: int, dest: int) -> float:
        minHeap = PriorityQueue()
        distTo = {node: float('inf') for node in (graph.graph)}
        parentEdge = {node: -1 for node in (graph.graph)}
        distTo[source] = 0
        parentEdge[source] = source

        minHeap.push(source, 0)

        while not minHeap.is_empty():
            curr_node, curr_dist = minHeap.pop()

            for neighbourgh in graph.graph[curr_node]:
                new_dist = curr_dist + graph.weight[(curr_node, neighbourgh)]
                if new_dist < distTo[neighbourgh]:
                    distTo[neighbourgh] = new_dist
                    parentEdge[neighbourgh] = curr_node
                    minHeap.push(neighbourgh,new_dist)

        return distTo[dest]

class Bellman_Ford(SPAlgorithm):
    def calc_sp(self, graph: WeightedGraph, source: int, dest: int) -> float:
        hashmap = {i: float('inf') for i in range (graph.get_num_of_nodes())}
        previous = {i: None for i in range (graph.get_num_of_nodes())}

        hashmap[source] = 0
        # Previous node of the source would be itself
        previous[source] = source

        # Performing at most n - 1 edge relaxations
        for _ in range (graph.get_num_of_nodes()-1):
            for u,v,weight in graph.weight:
                if hashmap[u] + weight < hashmap[v]:
                    hashmap[v] = hashmap[u] + weight
                    previous[v] = u
        
        for u,v,weight in graph.weight:
            if hashmap[u] + weight < hashmap[v]:
                print("Negative cycle detected")
                return
        
        return hashmap[dest]
    
class A_Star(SPAlgorithm):
    def calc_sp(self, graph: HeuristicGraph, source: int, dest: int):
        result = A.A_Star(graph, source,  dest, graph.get_heuristic())
        ##Result[1] is the path from source to dest
        path = result[1]
        weight = 0
        ##Go through the path, and add the weight of each edge to the return result
        for node in range(len(path)-1):
            weight += graph.weight[node,node+1]
        return weight
    

class ShortPathFinder():
    def __init__(self, graph: Graph, SPA: SPAlgorithm):
        self.graph = graph
        self.SPA = SPA
        
    def calc_short_path(self,source:int,dest:int)->float:
        self.SPA.calc_sp(self.graph,source,dest)

    def set_graph(self, graph: Graph):
        self.graph = graph

    def set_algorithm(self, algorithm: SPAlgorithm):
        self.SPA = algorithm