from node import Node
from edge import Edge
from import_data import load_df

def run_astar(start_node, end_node, distance_pr, demand_pr, cross_pr):
    distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
    demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
    distances_df = load_df(distances_df_pkl)
    demands_df = load_df(demands_df_pkl)
    dist_h_fun, dist_c_fun, dist_o_fun = init_distance_heuristic_cost_and_objective_function(distances_df, end_node)
    dem_h_fun, dem_c_fun, dem_o_fun = init_demand_heuristic_cost_and_objective_function(distances_df)
    objective_function = []
    curr_dist_node = start_node
    curr_dem_node = start_node
    while curr_dist_node != end_node or curr_dem_node != end_node:
        if curr_dist_node != end_node:
            dist_h_fun, dist_c_fun, dist_o_fun, dist_neighbors = dist_obj_fun_update(curr_dist_node, dist_h_fun, dist_c_fun, dist_o_fun)
        if curr_dem_node != end_node:
            dem_h_fun, dem_c_fun, dem_o_fun, dem_neighbors = dem_obj_fun_update(curr_dem_node, dem_h_fun, dem_c_fun, dem_o_fun)
                
        next_dist_node, next_dem_node = choose_next_node(end_node, curr_dist_node, curr_dem_node, dist_o_fun, dem_o_fun, dist_neighbors, dem_neighbors, cross_pr, distance_pr, demand_pr)
        print("Current dist node:")
        print(curr_dist_node)
        print("Current dem node:")
        print(curr_dem_node)
        print("Next dist node:")
        print(next_dist_node)
        print("Next dem node:")
        print(next_dem_node)
        curr_dist_node = next_dist_node
        curr_dem_node = next_dem_node
        
def choose_next_node(end_node, curr_dist_node, curr_dem_node, dist_o_fun, dem_o_fun, dist_neighbors, dem_neighbors, cross_pr, distance_pr, demand_pr):
    dem_next_node = None
    dist_next_node = None
    # checking path cross
    if curr_dist_node == curr_dem_node:
        for dist_neighbor in dist_neighbors:
            for dem_neighbor in dem_neighbors:
                if dist_neighbor == dem_neighbor:
                    # penalty for path cross
                    if curr_dist_node != end_node:
                        dist_o_fun[dist_neighbor] += cross_pr
                    if curr_dem_node != end_node:
                        dem_o_fun[dem_neighbor] += cross_pr
    
    # potential penalties applied
    min_cost = 100000
    min_dist_neighbor = None
    min_dem_neighbor = None
    for dist_neighbor in dist_neighbors:
        for dem_neighbor in dem_neighbors:
            print("DIST NEIGHBOR")
            print(dist_neighbor)
            print("DEM NEIGHBOR")
            print(dem_neighbor)
            print("DIST O FUN")
            print(dist_o_fun[dist_neighbor])
            print(dist_o_fun[dist_neighbor]*distance_pr)
            print("DEM O FUN")
            print(dem_o_fun[dem_neighbor])
            print(dem_o_fun[dem_neighbor]*demand_pr)
            
            temp_cost = dist_o_fun[dist_neighbor]*distance_pr + dem_o_fun[dem_neighbor]*demand_pr
            print("TEMP COST")
            print(temp_cost)
            if min_cost > temp_cost:
                min_cost = temp_cost
                if curr_dist_node != end_node: 
                    min_dist_neighbor = dist_neighbor
                else:
                    min_dist_neighbor = curr_dist_node
                if curr_dem_node != end_node:
                    min_dem_neighbor = dem_neighbor
                else:
                    min_dem_neighbor = curr_dem_node
    return min_dist_neighbor, min_dem_neighbor
    
def dist_obj_fun_update(curr_node, h_fun, c_fun, o_fun):
    curr_node = Node(curr_node)
    print("CURR DIST")
    print(curr_node.get_name())

    neighbors = curr_node.find_neighbors()    
    for neighbor in neighbors:
        neighbor = Node(neighbor)
        edge = Edge(curr_node.get_name(), neighbor.get_name())
        distance = edge.get_distance()
        c_fun[neighbor.get_name()] = c_fun[curr_node.get_name()] + distance
        o_fun[neighbor.get_name()] = h_fun[neighbor.get_name()] + c_fun[neighbor.get_name()]
    return h_fun, c_fun, o_fun, neighbors
        
def dem_obj_fun_update(curr_node, h_fun, c_fun, o_fun):    
    curr_node = Node(curr_node)
    neighbors = curr_node.find_neighbors()    
    for neighbor in neighbors:
        neighbor = Node(neighbor)
        edge = Edge(curr_node.get_name(), neighbor.get_name())
        demand = edge.get_demand()
        c_fun[neighbor.get_name()] = c_fun[curr_node.get_name()] + demand
        o_fun[neighbor.get_name()] = h_fun[neighbor.get_name()] + c_fun[neighbor.get_name()]
    return h_fun, c_fun, o_fun, neighbors

def init_distance_heuristic_cost_and_objective_function(distances_df, end_node):
    heuristic_function = {}
    cost_function = {}
    objective_function = {}
    nodes = list(distances_df.columns)[:-1]
    for node in nodes:
        node = Node(node)
        geo_distance = node.get_geo_distance(end_node)
        # update of heuristic function for all nodes 
        heuristic_function[node.get_name()] = geo_distance
        # update of cost function for all nodes 
        cost_function[node.get_name()] = 0
    for key, value in heuristic_function.items():
        objective_function[key] = value + cost_function[key]
    return heuristic_function, cost_function, objective_function
        
def init_demand_heuristic_cost_and_objective_function(distances_df):
    heuristic_function = {}
    cost_function = {}
    objective_function = {}
    nodes = list(distances_df.columns)[:-1]
    for node in nodes:
        node = Node(node)
        heuristic_function[node.get_name()] = 0
        cost_function[node.get_name()] = 0
    for key, value in heuristic_function.items():
        objective_function[key] = value + cost_function[key]
    return heuristic_function, cost_function, objective_function

# TEST EXAMPLE
start_node = "Aachen"
end_node = "Nuernberg"
distance_pr = 1
demand_pr = 1
cross_pr = 20
run_astar(start_node, end_node, distance_pr, demand_pr, cross_pr)