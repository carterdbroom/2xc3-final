import csv
import graph
import math
import AStar

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

        
        calculate_heuristic(connections_graph, goal_station, stations_data)

    return connections_graph


def build_graph_2(connections_data, stations_data):
    station_ids = [int(row['id']) for row in stations_data]

    connections_graph = graph.WeightedGraphAStar(station_ids)
    for row in connections_data:
        coordinate1 = get_station_coords(stations_data, row['station1'])
        coordinate2 = get_station_coords(stations_data, row['station2'])
        weight = euclidean_dist(coordinate1,coordinate2)

        connections_graph.add_edge(int(row['station1']), int(row['station2']), weight)

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


def find_adjacent_lines():
    # Loop through and get all stations that are on the same line
    # Adjacent lines, pick a station that has 2 or more lines connected through them, then pick another station from one of the lines, pick a 2nd station on the other line, compare their path length

    return

london_connections_data = parse_csv("london_connections.csv")
london_stations_data = parse_csv("london_stations.csv")


test_graph = build_graph(london_connections_data,london_stations_data, 70)



test_dict = station_lines(london_connections_data,london_stations_data)
print(test_dict)

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

print(all_pairs_a_star(graph1))

