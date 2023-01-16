import pandas as pd
from import_data import load_df
from pyvis.network import Network
from math import isnan

def add_distance_edges(net, distances_df):
    start_nodes_ids = net.get_nodes()
    end_nodes_ids = net.get_nodes()
    for start_node_id in start_nodes_ids:
        start_node_name = net.get_node(start_node_id)['label']
        if start_node_name == 'Cities':
            pass
        else:
            for end_node_id in end_nodes_ids:
                end_node_name = net.get_node(end_node_id)['label']
                if start_node_name == 'Cities':
                    pass
                else:
                    print(distances_df.index[distances_df['Cities'] == end_node_name].tolist())
                    try:
                        row_id = distances_df.index[distances_df['Cities'] == end_node_name].tolist()[0]
                        distance = distances_df.iloc[row_id][start_node_name]
                        net.add_edge(start_node_id, end_node_id, value=distance)
                    except:
                        pass
    net.show('distance_net.html')
    return net

def add_cost_edges(net, costs_df):
    start_nodes_ids = net.get_nodes()
    end_nodes_ids = net.get_nodes()
    for start_node_id in start_nodes_ids:
        start_node_name = net.get_node(start_node_id)['label']
        if start_node_name == 'Cities':
            pass
        else:
            for end_node_id in end_nodes_ids:
                end_node_name = net.get_node(end_node_id)['label']
                if start_node_name == 'Cities':
                    pass
                else:
                    print(costs_df.index[costs_df['Cities'] == end_node_name].tolist())
                    try:
                        row_id = costs_df.index[costs_df['Cities'] == end_node_name].tolist()[0]
                        cost = costs_df.iloc[row_id][start_node_name]
                        if isnan(cost) or cost == 0:
                            continue 
                        else:
                            net.add_edge(start_node_id, end_node_id, value=cost)
                    except:
                        pass
    net.show('cost_net.html')
    return net

def add_capacity_edges(net, capacities_df):
    start_nodes_ids = net.get_nodes()
    end_nodes_ids = net.get_nodes()
    for start_node_id in start_nodes_ids:
        start_node_name = net.get_node(start_node_id)['label']
        if start_node_name == 'Cities':
            pass
        else:
            for end_node_id in end_nodes_ids:
                end_node_name = net.get_node(end_node_id)['label']
                if start_node_name == 'Cities':
                    pass
                else:
                    print(capacities_df.index[capacities_df['Cities'] == end_node_name].tolist())
                    try:
                        row_id = capacities_df.index[capacities_df['Cities'] == end_node_name].tolist()[0]
                        capacity = capacities_df.iloc[row_id][start_node_name]
                        if isnan(capacity) or capacity == 0:
                            continue 
                        else:
                            net.add_edge(start_node_id, end_node_id, value=capacity)
                    except:
                        pass
    net.show('capacity_net.html')
    return net

def add_demand_edges(net, demand_df):
    start_nodes_ids = net.get_nodes()
    end_nodes_ids = net.get_nodes()
    for start_node_id in start_nodes_ids:
        start_node_name = net.get_node(start_node_id)['label']
        if start_node_name == 'Cities':
            pass
        else:
            for end_node_id in end_nodes_ids:
                end_node_name = net.get_node(end_node_id)['label']
                if start_node_name == 'Cities':
                    pass
                else:
                    try:
                        row_id = demand_df.index[demand_df['Cities'] == end_node_name].tolist()[0]
                        demand = demand_df.iloc[row_id][start_node_name]
                        # print(demand)
                        if not isinstance(demand, str):
                            if isnan(demand) is True:
                                continue                         
                        else:
                            net.add_edge(start_node_id, end_node_id, value=demand)
                    except:
                        pass
                        
    net.show('demand_net.html')
    return net

distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
capacities_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/capacities_df.pkl"
costs_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/costs_df.pkl"

distances_df = load_df(distances_df_pkl)
demands_df = load_df(demands_df_pkl)
capacities_df = load_df(capacities_df_pkl)
costs_df = load_df(costs_df_pkl)

nodes_names = list(distances_df.columns)
nodes_ids = list(range(len(nodes_names)))
net = Network()
for i in range(len(nodes_ids)):
    net.add_node(nodes_ids[i], label=nodes_names[i])
net.show('nodes.html')
# add_distance_edges(net, distances_df)
# add_cost_edges(net, costs_df)
# add_capacity_edges(net, capacities_df)
add_demand_edges(net, demands_df)

# print(demands_df.head(20))