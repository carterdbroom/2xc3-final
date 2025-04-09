import csv
import graph
import math
import AStar
import matplotlib.pyplot as plt

# Simple function using the csv library to parse a csv file and store its rows as dictionaries where the key are the column headers
# These dictionaries are then stored in a list/array
def parse_csv(filename):
    rows = []
    with open(filename, mode='r', newline='') as csvfile:
        file = csv.DictReader(csvfile, delimiter=',')
        for row in file:
            rows.append(row)

    return rows

# Function that is used to build the graph based on the connections and station data from the two given csv files
# It uses the heuristic graph or WeightedAStar graph class we defined in our graph.py file
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

# Linearly searches the stations data array because the csv file for station data isn't sorted (GOD WHY? IT SHOULD'VE BEEN SORTED!)
# When it find the station id we're looking for it returns a tuple of longitude and latitude
def get_station_coords(stations_data, station_id):
    for row in stations_data:
        if row['id'] == station_id:
            longitude = float(row['longitude'])
            latitude = float(row['latitude'])
            return (longitude,latitude)
    
    return None

# Euclidean distance equation to calculate the driving distance if two stations have a connection
# If they don't have a connection then we use it to calculate the heuristic as well. 
def euclidean_dist(coordinate1,coordinate2):
    distance = math.sqrt((coordinate2[0]-coordinate1[0])**2 + (coordinate2[1]-coordinate1[1])**2)
    return distance

# Find the driving distance and heuristic value using euclidean distance
def calculate_direct_distance(source_station, goal_station, stations_data):
    coordinate1 = get_station_coords(stations_data, source_station)
    coordinate2 = get_station_coords(stations_data, goal_station)

    direct_distance = euclidean_dist(coordinate1,coordinate2)

    return direct_distance

# Used to calculate a dictionary storing heuristic values for the given goal_station
def calculate_heuristic(graph, goal_station, stations_data):
    total_heuristic = {}
    for key in graph.graph.keys():
        distance = calculate_direct_distance(str(key), str(goal_station), stations_data)
        total_heuristic[key] = distance

    return total_heuristic


# Generates the shortest path between every single possible pair of source and destination stations in the subway system
def all_pairs_a_star(graph):
    all_paths = {}
    
    for i in graph.graph.keys():
        all_paths[i] = {}

    # This uses the A_star implementation that we made in our AStar file
    for destination in graph.graph.keys():
        total_heuristic = calculate_heuristic(graph, destination, london_stations_data)
        for source in graph.graph.keys():           
            all_paths[source][destination] = AStar.A_Star(graph, source, destination, total_heuristic)

    return all_paths            

# This function here is used to count the number of transfers taken by a certain path
def count_num_transfers(path, connections_line_data):
    transfers = 0

    # Returns 0 since there are self loops in our data
    if not path or len(path) < 2:
        return 0
    
    current_line = connections_line_data[(path[0],path[1])]

    # Looping through every station in the path (like a sliding window solution) and check if any line changes were taken 
    for i in range (1,len(path) - 1):
        # We can check this because we store the line of every connection in our A star graph
        next_line = connections_line_data[(path[i],path[i+1])]
        common_lines = current_line.intersection(next_line)
        if len(common_lines) == 0:
            transfers += 1
            current_line = next_line

    return transfers

# Used to find which lines each connection is connected through since there are duplicates in the data set
def connection_lines(connections_data):
    connection_lines_dictionary = {}
    for row in connections_data:
        if (row['station1'], row['station2']) not in connection_lines_dictionary:
            connection_lines_dictionary[(int(row['station1']), int(row['station2']))] = set()
            connection_lines_dictionary[(int(row['station1']), int(row['station2']))].add(int(row['line']))
        else:
            connection_lines_dictionary[(int(row['station1']), int(row['station2']))].add(int(row['line']))

        if  (row['station2'], row['station1']) not in connection_lines_dictionary:
            connection_lines_dictionary[(int(row['station2']), int(row['station1']))] = set()
            connection_lines_dictionary[(int(row['station2']), int(row['station1']))].add(int(row['line']))
        else:
            connection_lines_dictionary[(int(row['station2']), int(row['station1']))].add(int(row['line']))

    return connection_lines_dictionary


# Tally up the number of transfers taken by each path so that we can use this data to plot the distribution histogram
def build_histogram(graph, connections_data):
    all_pair_paths = all_pairs_a_star(graph)
    transfer_count = {}

    connection_lines_data = connection_lines(connections_data)

    for source, destination_dict in all_pair_paths.items():
        for destination, data in destination_dict.items():
            if source < destination:
                path = data[1]

                num_transfers = count_num_transfers(path, connection_lines_data)
                # If the current number of transfers is not a key in the dictionary, then initialize an entry in the dictionary
                # with that number of transfers as the key with a default value of 1 since there is 1 path that took this many
                # transfers
                if num_transfers not in transfer_count:
                    transfer_count[num_transfers] = 1
            
                else:
                    transfer_count[num_transfers] += 1

    draw_histogram(transfer_count)      
    return

# Simple function to draw our distribution histogram
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

london_connections_data = parse_csv("london_connections.csv")
london_stations_data = parse_csv("london_stations.csv")

graph1 = build_graph_2(london_connections_data, london_stations_data)

print(graph1.graph)
build_histogram(graph1, london_connections_data)
