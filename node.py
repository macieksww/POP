from import_data import load_df
from math import isnan

class Node:
    def __init__(self, name):
        distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
        demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
        capacities_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/capacities_df.pkl"
        self.capacities_df = load_df(capacities_df_pkl)
        self.distances_df = load_df(distances_df_pkl)
        self.demands_df = load_df(demands_df_pkl)
        self.name = name
        
    def get_name(self):
        return self.name
    
    def find_neighbors(self):
        neighbors = []
        cities = list(self.capacities_df.columns)[:-1]
        capacities = list(self.capacities_df[self.name])
        for i in range(len(capacities)):
            if not(isnan(capacities[i])):
                neighbors.append(cities[i])
        return neighbors
        
    def get_geo_distance(self, end_node):
        end_node = Node(end_node)
        row_id = self.distances_df.index[self.distances_df['Cities'] == end_node.get_name()].tolist()[0]
        distance = self.distances_df.iloc[row_id][self.name]
        return distance
        
        
        
# n = Node("Braunschweig")
# n.find_neighbors()