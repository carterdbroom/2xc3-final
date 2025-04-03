import csv
import graph

def parse_csv(filename):
    rows = []
    with open(filename, mode='r', newline='') as csvfile:
        file = csv.DictReader(csvfile, delimiter=',')
        for row in file:
            rows.append(row)

    return rows

london_connections_data = parse_csv("london_connections.csv")
london_stations_data = parse_csv("london_stations.csv")

print(london_connections_data)
print(london_stations_data)



def build_graph(connections, stations):
    connections_graph = graph.WeightedGraph()
    for row in connections:
        connections_graph.add_edge(row['station1'],row['station2'],row['time'])
    
    
    return
