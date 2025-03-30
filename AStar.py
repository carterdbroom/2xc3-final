from AllPairs import PriorityQueue
import random
import math
# For the heuristic function we will use Euclidean Distance Heuristics. 
# h = sqrt( (current_cell.x - goal.x)**2 + (current_cell.y - goal.y)**2)

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}

    def push(self, item, priority):
        # Append new element and restore the heap property by sifting up
        self.heap.append((priority, item))
        self.entry_finder[item] = priority
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        # Remove and return the element with the smallest priority
        if not self.heap:
            raise IndexError("pop from empty priority queue")
        # Swap the first element with the last, remove the last element
        self._swap(0, len(self.heap) - 1)
        # Also note that heap is a list and this is not a recursive call, just a pop on a list, confused me for a second.
        priority, item = self.heap.pop()
        # Removing the we are popping from the dictionary.
        del self.entry_finder[item]
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

class WeightedGraph():
    def __init__(self, nodes, coordinates):
        self.graph = {}
        self.weight = {}
        self.coordinate = {}
        for i in range(nodes):
            self.graph[i] = []
            self.coordinate[i] = coordinates[i]

    def are_connected(self, node1, node2):
        for node in self.graph[node1]:
            if node == node2:
                return True
        return False

    def connected_nodes(self, node):
        return self.graph[node]

    def add_node(self, x, y):
        #add a new node number = length of existing node
        self.graph[len(self.graph)] = []
        self.coordinate[len(self.coordinate)] = (x, y)

    def add_edge(self, node1, node2):
        if node1 not in self.graph[node2]:
            self.graph[node1].append(node2)
            # Since we are adding coordinates we have to make the edges weights based on the coordinates. 
            weight_between = euclidean_distance(self.coordinate[node1][0], self.coordinate[node1][1], self.coordinate[node2][0], self.coordinate[node2][1])
            self.weight[(node1, node2)] = weight_between


            #since it is undirected
            self.graph[node2].append(node1)
            self.weight[(node2, node1)] = weight_between

    def number_of_nodes(self,):
        return len(self.graph)

    def has_edge(self, src, dst):
        return dst in self.graph[src] 
    
    # Added this to check the weight as well.
    def has_edge_with_weight(self, src, dst, weight):
        return dst in self.graph[src] and self.weight[(src, dst)] == weight

    def get_weight(self,):
        total = 0
        for node1 in self.graph:
            for node2 in self.graph[node1]:
                total += self.weight[(node1, node2)]
                
        # because it is undirected
        return total/2

# Here is the function that creates random graphs. 
def create_random_weighted_graph(nodes, edges):
    # Creating random coordinates for each node. Say we have one node, if we have a range from 
    # 0 to 1, we can fit 4 different nodes in that space. We want spread our graph out a bit, 
    # So we multiply the upper end by 4. 
    coordinates = []
    for i in range(nodes):
        while True: 
            potential_coordinate = (random.randint(0, 4*nodes), random.randint(0, 4*nodes))
            if potential_coordinate not in coordinates: 
                coordinates.append(potential_coordinate)
                break
    # Creating all the nodes in the graph, no edges connecting them
    graph = WeightedGraph(nodes, coordinates)
    # The max number of edges is n choose 2. We also add n since we are allowing self loops
    if edges > (nodes + (nodes*(nodes - 1))//2): 
        print("There cannot be double edges in your graph, there must be less edges than nodes!")
        return graph

    # We create the given amount of edges in the graph.
    for _ in range(edges):
        # We want to continue to try and find suitable nodes until we do.
        while True:
            # We choose two random nodes for the edge to run between.
            node1 = random.randint(0, nodes - 1)
            node2 = random.randint(0, nodes - 1)
            # We have to make the weight based on the euclidean distance between the nodes. 
            weight1 = euclidean_distance(graph.coordinate[node1][0], graph.coordinate[node1][1], graph.coordinate[node2][0], graph.coordinate[node2][1])

            # If the graph does not have the edge we have generated, then we add it to the graph.
            # We break the "while True" statement to continue onto the next edge. 
            # Otherwise, we continue this process by generating two new nodes.
            if not graph.has_edge(node1, node2):
                graph.add_edge(node1, node2)
                break
    return graph

# This calculates the euclidean distance between two points. We will use this as the heuristic.
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# This is intended to be used as a heuristic, where we have a graph and a destination node. For every node in the graph we 
# determine its distance from the destination node. 
def calculate_heuristic(graph, destination): 
    heuristic = []
    # Calculates the euclidean distance from the destination node to all other nodes in the graph. 
    for i in range(len(graph.coordinate)): 
        distance_from_destination = euclidean_distance(graph.coordinate[destination][0], graph.coordinate[destination][1], graph.coordinate[i][0], graph.coordinate[i][1])
        heuristic.append(distance_from_destination)
    return heuristic

# This algorithm finds the shortest path between a source node and a destination node. 
def A_Star(graph, source, destination, heuristic): 

    # Creating dictionaries for the g score (the actual weight between nodes) and the f score (which is the weight plus the heuristic).
    g_score = {i : float('inf') for i in range(len(graph.graph))}
    g_score[source] = 0
    f_score = {i : float('inf') for i in range(len(graph.graph))}
    f_score[source] = heuristic[source]

    # Creating a heap and pushing the value of g (which is 0) and then the value of h (which we get from our heuristic).
    heap = PriorityQueue()
    heap.push(source, 0 + heuristic[source])

    # This will keep track of where each node came from.
    came_from = {}

    # We keep searching for shortest paths until our heap is empty, or if we find the goal node. 
    while not heap.is_empty():
        
        # Popping the top element off the heap. This is the element with the smallest f score, which takes the actual
        # weight and the heuristic into account.
        current_node, current_total_score = heap.pop()

        # If we have reached our destination node we return. 
        if current_node == destination: 
            return came_from
        
        # Iterating through all of the nodes that are connected to the node we are currently at. 
        for connecting_node in graph.graph[current_node]:
            potential_g_score = g_score[current_node] + graph.weight[(current_node, connecting_node)]         
            
            # If this is true, the path to this node is better than any we any we have found previously.
            if potential_g_score < g_score[connecting_node]: 
                came_from[connecting_node] = current_node
                g_score[connecting_node] = potential_g_score
                f_score[connecting_node] = potential_g_score + heuristic[connecting_node]

                # Not sure on this part may need to change it.
                # We want to add the element with the smallest, but right this just adds the first.
                if not heap.entry_finder[connecting_node]:
                    heap.push(connecting_node, f_score[connecting_node])
    return ()

# Given an dictionary that tracks where each node came from and a source and destination nodes, reconstructs the path that was taken.
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