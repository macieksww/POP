from xml.etree import ElementTree
from math import sqrt
import pandas as pd

network_data_path = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/sndlib-networks-native/germany50.txt"
instances_data_path = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/sndlib-instances-native/germany50.txt"
data_path = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/germany50.xml"
distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
capacities_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/capacities_df.pkl"
costs_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/costs_df.pkl"

def save_df(df, pkl_path):
    df.to_pickle(pkl_path)
    
def load_df(pkl_path):
    df = pd.read_pickle(pkl_path)
    return df

def calculate_distance(nodes, nodes_crds):
    start_node = nodes[0]
    end_node = nodes[1]
    distance = sqrt((nodes_crds[start_node]['x']-nodes_crds[end_node]['x'])**2+(nodes_crds[start_node]['y']-nodes_crds[end_node]['y'])**2)
    return distance

def fetch_structure_data(data_path):
    nodes = []
    nodes_crds = {}
    structure, demands = list(ElementTree.parse(data_path).getroot())
    nodes_tag, links_tag = list(structure)

    # fetching info about nodes from xml file
    for node in nodes_tag:
        nodes.append(node.get("id"))
        for crds in node:
            nodes_crds[str(node.get("id"))] = {}
            for xy in crds:
                if str(xy.tag)[-1:] == "y":
                    nodes_crds[str(node.get("id"))]['y'] = float(xy.text)
                else:
                    nodes_crds[str(node.get("id"))]['x'] = float(xy.text)
    return (nodes, nodes_crds, links_tag)

def create_demands_df(data_path):
    global demands_df_pkl
    structure, demands = list(ElementTree.parse(data_path).getroot())
    nodes, nodes_crds, _ = fetch_structure_data(data_path)
    nodes_demands_df = pd.DataFrame()
    for node in nodes:
        nodes_demands_df[node] = []
    nodes_demands_df['Cities'] = nodes
    print(nodes_demands_df.head())
    for demand in demands:
        source = ""
        target = ""
        demand_value = 0
        for details in demand:
            if "source" in str(details.tag):
                source = details.text
            if "target" in str(details.tag):
                target = details.text
            if "demandValue" in str(details.tag):
                demand_value = details.text
    
        # filling up the demands dataframe
        row_id = nodes_demands_df.index[nodes_demands_df['Cities'] == target].tolist()[0]
        nodes_demands_df.at[row_id, source] = demand_value 
        print(nodes_demands_df.head()) 
            
    # saving demands df to file
    save_df(nodes_demands_df, demands_df_pkl)
    
def create_capacity_df(data_path):
    _, _, links = fetch_structure_data(data_path)
    nodes, nodes_crds, _ = fetch_structure_data(data_path)
    nodes_capacities_df = pd.DataFrame()
    for node in nodes:
        nodes_capacities_df[node] = []
    nodes_capacities_df['Cities'] = nodes
    nodes_costs_df = pd.DataFrame()
    for node in nodes:
        nodes_costs_df[node] = []
    nodes_costs_df['Cities'] = nodes
    
    for link in links:
        source = ""
        target = ""
        capacity = 0
        cost = 0
        for details in link:
            additional_modules = None
            print(details.tag)
            if "source" in str(details.tag):
                source = details.text
            if "target" in str(details.tag):
                target = details.text
                print(details.text)
            if "additionalModules" in str(details.tag):
                additional_modules = details[0]
                for am in additional_modules:
                    if "capacity" in str(am.tag):
                        capacity = float(am.text)
                    if "cost" in str(am.tag):
                        cost = float(am.text)
                        
        # filling up the costs dataframe
        row_id = nodes_costs_df.index[nodes_costs_df['Cities'] == target].tolist()[0]
        nodes_costs_df.at[row_id, source] = cost 
        print(nodes_costs_df.head()) 
        
        # filling up the capacities dataframe
        row_id = nodes_capacities_df.index[nodes_capacities_df['Cities'] == target].tolist()[0]
        nodes_capacities_df.at[row_id, source] = capacity 
        print(nodes_capacities_df.head()) 
        
    # saving costs df to file
    save_df(nodes_costs_df, costs_df_pkl)
    
    # saving capacities df to file
    save_df(nodes_capacities_df, capacities_df_pkl)        
            
def create_distances_df(nodes, nodes_crds):
    global distances_df_pkl
    # dataframe to store data about distances between locations
    nodes_dist_df = pd.DataFrame()
    for node in nodes:
        nodes_dist_df[node] = []
    nodes_dist_df['Cities'] = nodes
    print(nodes_dist_df.head())

    # filling up the distance dataframe
    for start_node in nodes_dist_df.columns:
        if start_node == 'Cities':
            pass
        else:
            for end_node in nodes_dist_df.columns:
                if end_node == 'Cities':
                    pass
                else:
                    distance = calculate_distance([start_node, end_node], nodes_crds)
                    row_id = nodes_dist_df.index[nodes_dist_df['Cities'] == end_node].tolist()[0]
                    nodes_dist_df.at[row_id, start_node] = distance 
                    print(nodes_dist_df.head()) 
    
    # saving distances df to file
    save_df(nodes_dist_df, distances_df_pkl)


(nodes, nodes_crds, _) = fetch_structure_data(data_path)
# create_distances_df(nodes, nodes_crds)
# create_demands_df(data_path)
# create_capacity_df(data_path)
