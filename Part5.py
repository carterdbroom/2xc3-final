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


def find_adjacent_lines():
    # Loop through and get all stations that are on the same line
    # Adjacent lines, pick a station that has 2 or more lines connected through them, then pick another station from one of the lines, pick a 2nd station on the other line, compare their path length

    return

london_connections_data = parse_csv("london_connections.csv")
london_stations_data = parse_csv("london_stations.csv")


test_graph = build_graph(london_connections_data,london_stations_data, 70)

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

print(graph1.graph)

def same_line(graph, stations_line_data, stations_data):
    same_line_paths_cost = {}

    for source in graph.graph.keys():
        for destination in graph.graph.keys():
            # We check this so that we only count the path once because going from destination to source is also a path the algorithm could take
            if source < destination:
                source_lines = stations_line_data.get(str(source))
                destination_lines = stations_line_data.get(str(destination))
                # Using basic set intersection method (I did not know this even existed before googling)
                lines_in_common = source_lines.intersection(destination_lines)

                # Check to see if there are lines in common at all between the pair of stations the loop is currently examining
                if lines_in_common:
                    heuristic_value = calculate_heuristic(graph, destination, stations_data)
                    # Came_from is not used here but it is returned by A* so we just left it there as a dummy variable so that we can grab path
                    came_from, path = AStar.A_Star(graph,source,destination, heuristic_value)

                    #Check to see if there is even a path returned by A*
                    if path:
                        cost = path_cost(path,graph)
                        same_line_paths_cost[(source,destination)] = {'lines_in_common': lines_in_common, 'path': path, 'total_cost': cost}

    return  same_line_paths_cost


# Helper function here to help calculate the cost of a path
def path_cost(path, graph):
    cost = 0
    # Sums up the weight from the source node to the next one in the path and increments for the whole path until the end
    for i in range (len(path) - 1):
        cost += graph.weight[(path[i],path[i + 1])]
    
    return cost