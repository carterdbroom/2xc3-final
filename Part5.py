import csv
import graph
import math
import AStar
import matplotlib.pyplot as plt

def parse_csv(filename):
    rows = []
    with open(filename, mode='r', newline='') as csvfile:
        file = csv.DictReader(csvfile, delimiter=',')
        for row in file:
            rows.append(row)

    return rows


def build_graph(connections_data, stations_data, goal_station):
    station_ids = [int(row['id']) for row in stations_data]

    connections_graph = graph.WeightedGraphAStar(station_ids)
    for row in connections_data:
        coordinate1 = get_station_coords(stations_data, row['station1'])
        coordinate2 = get_station_coords(stations_data, row['station2'])
        weight = euclidean_dist(coordinate1,coordinate2)
        line = row['line']

        connections_graph.add_edge(int(row['station1']), int(row['station2']), weight, line)

    return connections_graph


def build_graph_2(connections_data, stations_data):
    station_ids = [int(row['id']) for row in stations_data]

    connections_graph = graph.WeightedGraphAStar(station_ids)
    for row in connections_data:
        coordinate1 = get_station_coords(stations_data, row['station1'])
        coordinate2 = get_station_coords(stations_data, row['station2'])
        weight = euclidean_dist(coordinate1,coordinate2)
        line = row['line']

        connections_graph.add_edge(int(row['station1']), int(row['station2']), weight, line)

    return connections_graph

def get_station_coords(stations_data, station_id):
    for row in stations_data:
        if row['id'] == station_id:
            longitude = float(row['longitude'])
            latitude = float(row['latitude'])
            return (longitude,latitude)
    
    return None

def euclidean_dist(coordinate1,coordinate2):
    distance = math.sqrt((coordinate2[0]-coordinate1[0])**2 + (coordinate2[1]-coordinate1[1])**2)
    return distance

def calculate_direct_distance(source_station, goal_station, stations_data):
    coordinate1 = get_station_coords(stations_data, source_station)
    coordinate2 = get_station_coords(stations_data, goal_station)

    direct_distance = euclidean_dist(coordinate1,coordinate2)

    return direct_distance

def station_lines(london_connections_data, london_stations_data):
    station_lines_dictionary = {}

    for row1 in london_stations_data:
        station_lines_dictionary[row1['id']] = set()


    for row in london_connections_data:
        station_lines_dictionary[row['station1']].add(row['line'])
        station_lines_dictionary[row['station2']].add(row['line'])

    return station_lines_dictionary

london_connections_data = parse_csv("london_connections.csv")
london_stations_data = parse_csv("london_stations.csv")

#print(test_graph.graph)
#print(test_graph.heuristic)

def calculate_heuristic(graph, goal_station, stations_data):
    total_heuristic = {}
    for key in graph.graph.keys():
        distance = calculate_direct_distance(str(key), str(goal_station), stations_data)
        total_heuristic[key] = distance

    return total_heuristic

graph1 = build_graph_2(london_connections_data, london_stations_data)

# Generates all pairs
def all_pairs_a_star(graph):
    all_paths = {}
    
    for i in graph.graph.keys():
        all_paths[i] = {}

    for destination in graph.graph.keys():
        total_heuristic = calculate_heuristic(graph, destination, london_stations_data)
        for source in graph.graph.keys():           
            all_paths[source][destination] = AStar.A_Star(graph, source, destination, total_heuristic)

    return all_paths            


#print(all_pairs_a_star(graph1))

#same_line_path_cost = same_line(graph1,station_lines_data,london_stations_data)
#print(same_line_path_cost)

def count_num_transfers(path, graph):
    transfers = 0

    if not path or len(path) < 2:
        return 0
    
    current_line = graph.line.get((path[0],path[1]))

    for i in range (1,len(path) - 1):
        next_line = graph.line.get((path[i],path[i+1]))
        if next_line != current_line:
            transfers += 1
            current_line = next_line

    return transfers


def build_histogram(graph):
    all_pair_paths = all_pairs_a_star(graph)
    transfer_count = {}

    for source, destination_dict in all_pair_paths.items():
        for destination, data in destination_dict.items():
            if source < destination:
                path = data[1]
            
                num_transfers = count_num_transfers(path,graph)
                if num_transfers not in transfer_count:
                    transfer_count[num_transfers] = 1
            
                else:
                    transfer_count[num_transfers] += 1

    draw_histogram(transfer_count)      
    return

def draw_histogram (transfer_count):
    keys = sorted(transfer_count.keys())
    values = [transfer_count[k] for k in keys]

    fig=plt.figure(figsize=(20,8))
    plt.bar(keys,values)
    plt.xticks(keys)

    plt.xlabel("Number of Transfers made")
    plt.ylabel("Number of paths that made each number of transfers")
    plt.title("Distribution of Transfers made in each shortest path")

    plt.savefig("Distribution.png")
    plt.show()

    return

print(graph1.graph)
build_histogram(graph1)
