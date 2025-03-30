from AllPairs import PriorityQueue
import random
import math
# For the heuristic function we will use Euclidean Distance Heuristics. 
# h = sqrt( (current_cell.x - goal.x)**2 + (current_cell.y - goal.y)**2)


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

def A_Star(graph, source, heuristic): 
    predecessor = {}
    heuristic = {}

# Heuristic calculation 

# At every node, assign a value of h. This value h will be the euclidean distance from 
# the current node to the source node we are trying to find. 

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)