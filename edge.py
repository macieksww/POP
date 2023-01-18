from import_data import load_df
from node import Node
from math import isnan

class Edge:
    def __init__(self, start_node, end_node):
        distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
        demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
        capacities_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/capacities_df.pkl"
        self.capacities_df = load_df(capacities_df_pkl)
        self.distances_df = load_df(distances_df_pkl)
        self.demands_df = load_df(demands_df_pkl)
        self.start_node = Node(start_node)
        self.end_node = Node(end_node)
        self.distance = 0
        
    def get_start_node(self):
        return self.start_node
    
    def get_end_node(self):
        return self.end_node
    
    def edge_exists(self):
        row_id = self.capacities_df.index[self.capacities_df['Cities'] == self.end_node.get_name()].tolist()[0]
        capacity = self.capacities_df.iloc[row_id][self.start_node.get_name()]
        if isnan(capacity):
            return False
        else:
            return True
    
    def get_distance(self):
        row_id = self.distances_df.index[self.distances_df['Cities'] == self.end_node.get_name()].tolist()[0]
        distance = self.distances_df.iloc[row_id][self.start_node.get_name()]
        return distance
    
    def get_demand(self):
        row_id = self.demands_df.index[self.demands_df['Cities'] == self.end_node.get_name()].tolist()[0]
        demand = self.demands_df.iloc[row_id][self.start_node.get_name()]
        # if demand is Nan, it means that there is no demand, but still, a link can exist
        # between given locations, than set demand to 0
        if isnan(demand):
            demand = 0
        return demand 
        
