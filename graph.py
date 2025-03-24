
class Graph():
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


# Here is the function that creates random graphs. 
def create_random_graph(nodes, edges):
    # Creating all the nodes in the graph, no edges connecting them
    graph = Graph(nodes)

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
            weight1 = random.randint(0, nodes - 1)

            # If the graph does not have the edge we have generated, then we add it to the graph.
            # We break the "while True" statement to continue onto the next edge. 
            # Otherwise, we continue this process by generating two new nodes.
            # Added a check to see if the weight is valid too. 
            if not graph.has_edge(node1, node2) and not graph.has_edge_with_weight(node1, node2, weight1):
                graph.add_edge(node1, node2, weight1)
                break
    

    return graph
