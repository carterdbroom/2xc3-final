import graph

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        # Append new element and restore the heap property by sifting up
        self.heap.append((priority, item))
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        # Remove and return the element with the smallest priority
        if not self.heap:
            raise IndexError("pop from empty priority queue")
        # Swap the first element with the last, remove the last element
        self._swap(0, len(self.heap) - 1)
        priority, item = self.heap.pop()
        # Restore the heap property by sifting down from the root
        self._sift_down(0)
        return item, priority

    def is_empty(self):
        return len(self.heap) == 0

    def _sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index):
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


def dijkstra(graph, source, relaxed):
    distances = {node: float('inf') for node in graph.graph}
    distances[source] = 0

    minHeap = PriorityQueue()

    minHeap.push(source, 0)

    while not minHeap.is_empty:
        current_node, current_distance = minHeap.pop()
        
        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.graph[current_node]:
            if (current_node, neighbor) in relaxed:
                new_distance = current_distance + relaxed[(current_node, neighbor)]
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    minHeap.push(neighbor,new_distance)

    return distances


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


def allPair(graph):
    n = graph.number_of_nodes()

    edges = []
    for u in graph.graph():
        for v in graph.graph[u]:
            weight = graph.weights[(u,v)]
            edges.append((u,v,weight))

    for v in range(n):
        edges.append((n,v,0))
    
    num_nodes = n + 1

    hashmap = bellman_ford(num_nodes, edges, n)
    relaxed = {}

    for u,v,weight in edges:
        if u == n:
            continue
        
        relaxed[(u,v)] = weight + hashmap[u] - hashmap[v]
    
    all_pairs = {}

    for u in range(n):
        relaxed_edges = dijkstra(graph, u, relaxed)
        all_pairs[u] = {}

        for v in range (n):
            # Check if the node has been reached or not
            if relaxed_edges[v] < float('inf'):
                distance = relaxed_edges[v] - hashmap[u] + hashmap[v]
                all_pairs[u][v] = distance
            else:
                all_pairs[u][v] = float('inf')
    
    return all_pairs