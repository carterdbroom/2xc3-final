import random

# graph implementation using adjacency list   
class AdjacencyGraph():
    # using adjacency list
    def __init__(self, nodes):
        self.graph = []
        # node numbered 0-1
        for node in range(nodes):
            self.graph.append([])
        
    def has_edge(self, src, dst):
        return src in self.graph[dst]
    
    # We edited this function so that there is only one entry if there is a self loop.
    def add_edge(self,src,dst):
        if not self.has_edge(src,dst):
            self.graph[src].append(dst)
            if src != dst:
                self.graph[dst].append(src)
    
    def get_graph(self,):
        return self.graph
    
        # This is a modified DFS that checks for cycles.
    def has_cycle_helper(self, v, adj_list, visited_list, parent):
        visited_list[v] = True

        for i in adj_list[v]:
            if not visited_list[i]:
                if self.has_cycle_helper(i, adj_list, visited_list, v):
                    return True

            elif i != parent:
                return True

        return False 
    
    def has_cycle(self,):
        visited_list = [False for i in range(len(self.graph))]

        for i in range(len(self.graph)):
            
            if not visited_list[i]:
                if self.has_cycle_helper(i, self.graph, visited_list, -1):
                    return True
        return False

    def is_connected(self,node1,node2):
        # We check the first node since the predecessor dictionary does not include it in the keys.
        if node1 == node2:
            return True
        # This gives us the predecessor dictionary, so that will include everything except the first nodes.
        if node2 in DFS_3(self, node1).keys():
            return True
        return False

class WeightedGraph():
    def __init__(self, nodes):
        self.graph = {}
        self.weight = {}
        for i in range(nodes):
            self.graph[i] = []

    def are_connected(self, node1, node2):
        for node in self.adj[node1]:
            if node == node2:
                return True
        return False

    def connected_nodes(self, node):
        return self.graph[node]

    def add_node(self,):
        #add a new node number = length of existing node
        self.graph[len(self.graph)] = []

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph[node2]:
            self.graph[node1].append(node2)
            self.weight[(node1, node2)] = weight

            #since it is undirected
            self.graph[node2].append(node1)
            self.weight[(node2, node1)] = weight

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
    
class WeightedGraphAStar():
    def __init__(self, nodes):
        self.graph = {}
        self.weight = {}
        self.heuristic = {}
        self.line = {}
        # Changed this part so that we pass in a list/array of station ids and we make each id a node in the graph and each node is a key in the graph dictionary
        for node in nodes:
            self.graph[node] = []

    def are_connected(self, node1, node2):
        # Checks if node2 is in the adjacency list of node1.
        for node in self.graph[node1]:
            if node == node2:
                return True
        return False

    def connected_nodes(self, node):
        return self.graph[node]

    def add_node(self):
        # If we want to add a node, we take the station_id with the highest number and + 1 to it to guarantee it's a unique station
        # Honestly, I don't think we are ever going to use this for part 5
        new_key = max(self.graph.keys()) + 1
        self.graph[new_key] = []

        return

    def add_edge(self, node1, node2, weight, line):
        # Adds an edge between node1 and node2 with the given weight.
        if node1 not in self.graph[node2]:
            self.graph[node1].append(node2)
            self.weight[(node1, node2)] = weight
            self.line[(node1,node2)] = line

            # Since it is undirected, add the reverse connection as well. (Might remove this but I think the station map she gave us is undirected, so idk)
            self.graph[node2].append(node1)
            self.weight[(node2, node1)] = weight
            self.line[(node2, node1)] = line
        
        return

    def add_heuristic(self, node, heuristic_value):
        self.heuristic[node] = heuristic_value
        return

    def number_of_nodes(self):
        return len(self.graph)

    def has_edge(self, src, dst):
        return dst in self.graph[src]
    
    def has_edge_with_weight(self, src, dst, weight):
        return dst in self.graph[src] and self.weight[(src, dst)] == weight

    def get_weight(self):
        total = 0
        for node1 in self.graph:
            for node2 in self.graph[node1]:
                total += self.weight[(node1, node2)]
        # Because it is undirected, each edge is counted twice.
        return total / 2

def create_random_adjacency_graph(nodes, edges):
    # Creating all the nodes in the graph, no edges connecting them
    graph = AdjacencyGraph(nodes)

    # The max number of edges is n choose 2. We also add n since we are allowing self loops
    if edges > (nodes + (nodes*(nodes - 1))/2): 
        print("There cannot be double edges in your graph, there must be less edges than nodes!")
        return  graph

    # We create the given amount of edges in the graph.
    for _ in range(edges):
        # We want to continue to try and find suitable nodes until we do.
        while True:
            # We choose two random nodes for the edge to run between.
            node1 = random.randint(0, nodes - 1)
            node2 = random.randint(0, nodes - 1)

            # If the graph does not have the edge we have generated, then we add it to the graph.
            # We break the "while True" statement to continue onto the next edge. 
            # Otherwise, we continue this process by generating two new nodes.
            if not graph.has_edge(node1, node2):
                graph.add_edge(node1, node2)
                break
    

    return graph

# Here is the function that creates random graphs. 
def create_random_weighted_graph(nodes, edges, high, low):
    # Creating all the nodes in the graph, no edges connecting them
    graph = WeightedGraph(nodes)

    # The max number of edges is n choose 2. We also add n since we are allowing self loops
    if edges > (nodes + (nodes*(nodes - 1))/2): 
        print("There cannot be double edges in your graph, there must be less edges than nodes!")
        return  graph

    # We create the given amount of edges in the graph.
    for _ in range(edges):
        # We want to continue to try and find suitable nodes until we do.
        while True:
            # We choose two random nodes for the edge to run between.
            node1 = random.randint(0, nodes - 1)
            node2 = random.randint(0, nodes - 1)
            weight1 = random.randint(low, high)

            # If the graph does not have the edge we have generated, then we add it to the graph.
            # We break the "while True" statement to continue onto the next edge. 
            # Otherwise, we continue this process by generating two new nodes.
            # Added a check to see if the weight is valid too. 
            if not graph.has_edge(node1, node2) and (node1 != node2):
                graph.add_edge(node1, node2, weight1)
                break
    

    return graph