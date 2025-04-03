import csv
import graph

def parse_csv_file(filename):
    rows = []
    with open(filename,mode='r', newline='') as csvfile:
        file = csv.DictReader(csvfile,delimiter=',')
        for row in file:
            rows.append(row)
    return rows

london_connections_data = parse_csv_file('london_connections.csv')

print(london_connections_data)

def build_graph(csv_data):
    
    return