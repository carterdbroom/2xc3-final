import graph

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        self.heap.append((priority, item))
        self.swim(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            print("Cannot remove from an empty heap")
            return 
        
        # Swap the first element with the last and then we remove the last element with pop
        self._swap(0, len(self.heap) - 1)
        priority, item = self.heap.pop()

        self.sink(0)
        return item, priority

    def is_empty(self):
        return len(self.heap) == 0

    def swim(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def sink(self, index):
        n = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph.graph}
    distances[source] = 0
    # Adding previous like the on that's in Floyd Warshall
    previous = {node: None for node in graph.graph}

    minHeap = PriorityQueue()

    minHeap.push(source, 0)

    while not minHeap.is_empty():
        current_node, current_distance = minHeap.pop()
        
        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.graph[current_node]:
            distance = current_distance + graph.weight[(current_node, neighbor)]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                minHeap.push(neighbor, distance)

    return distances, previous


def bellman_ford(num_nodes, edges, source):
    hashmap = {i: float('inf') for i in range (num_nodes)}

    hashmap[source] = 0

    # Performing at most n - 1 edge relaxations
    for _ in range (num_nodes-1):
        for u,v,weight in edges:
            if hashmap[u] + weight < hashmap[v]:
                hashmap[v] = hashmap[u] + weight
    
    for u,v,weight in edges:
        if hashmap[u] + weight < hashmap[v]:
            print("Negative cycle detected")
            return
    
    return hashmap

# Basically running Dijkstra's algorithm for V times where each pass we run it on a different source
# so we eventually run it with every node being a source one
def allPair(graph):
    shortest_paths = {}
    previous = {}
    for node in graph.graph.keys():
        shortest_paths[node], previous[node] = dijkstra(graph,node)
    
    return shortest_paths, previous

# Floyd Warshall's algorithm like the one from graded lab 2
def floyd_warshall(graph):
    n = graph.number_of_nodes()
    distances = [[float('inf')] * n for _ in range (n)]
    # Keeping track of a previous matrix since the question mentioned this
    previous = [[None] * n for _ in range (n)]

    # Set all self loops to weight 0 so the matrix has all 0 entries on the main diagonal
    for i in range (n):
        distances[i][i] = 0
    
    # Looping through the matrix and adding the weights at each position of the distances matrix
    for node in graph.graph:
        for neighbor in graph.graph[node]:
            distances[node][neighbor] = graph.weight[(node,neighbor)]
            previous[node][neighbor] = node
    
    # This part is the main part of the Floyd Warshall algorithm that was in graded lab 2
    for k in range (n):
        for i in range (n):
            for j in range (n):
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    previous[i][j] = previous[k][j]

    print(distances)
    print (previous)
    return distances, previous


graph1 = graph.create_random_weighted_graph(6, 12, 10, 1)
print(graph1.graph)
print(graph1.weight)
floyd_warshall(graph1)
