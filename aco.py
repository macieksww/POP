from import_data import load_df
from random import random
import pandas

# b -> influence of remaining data on the choice of the next vertex
# m -> number of ants
# t_min -> minimum acceptable amount of pheromones on the edges
# t_max -> maximum acceptable amount of pheromones on the edges
# t_0 -> initial amount of pheromones on the edges
# s -> initial vertex number
# t -> terminal vertex
# p -> speed of evaporation

def aco(start_v, end_v, vertices, m=10, t_0=0, vaporization_rate=0.9, theta=0.8):
    current_vertex = start_v
    global_path_found = False
    path_found = False
    (nodes_visited, visited_vertexes, current_vertexes, edges) = init_aco(start_v, end_v, vertices, m=10, t_0=0)
    for i in range(m):
        path_found = False
        while path_found is False:
            new_vertex = select_next_vertex(current_vertex, i, visited_vertexes, edges, vaporization_rate, theta)
            current_vertex = new_vertex
            visited_vertexes[i].append(current_vertex)
            if current_vertex == end_v:
                path_found = True
                print("Path found for route from " + str(start_v) + " to " + str(end_v) + " for ant: " + str(i))
    path = get_path(visited_vertexes, m-1)
    return path
    
def init_aco(start_v, end_v, vertices, m=10, t_0=0):
    # initialising egdes  with default pheromones level
    edges = []
    nodes_visited = {}
    visited_vertexes = {}
    current_vertexes = {}
    ants_routes = {}
    current_vertex = start_v
    for st_v in vertices:
        for end_v in vertices:
            edge = {"st_v": st_v,
                    "end_v": end_v,
                    "ph": t_0,
                    "visited": False}
            edges.append(edge)
        nodes_visited[st_v] = False
    
    # initialising ants
    for i in range(m):
        current_vertexes[i] = start_v
        visited_vertexes[i] = [start_v]
    return (nodes_visited, visited_vertexes, current_vertexes, edges)
        
# select next vertex
def select_next_vertex(start_v, ant_id, visited_vertexes, edges, vaporization_rate, theta):
    if len(find_neighbors(start_v)) == 0:
        print("Vertex has no neighbors")
    else:
        neighbors = find_neighbors(start_v)
        current_best_neighbor = ""
        current_highest_ph = 100000 
        for neighbor in neighbors:
            # if given neighbor vertex wasnt visited by the ant yet
            # choice of a best neighbor with respect to pheromone level
            if neighbor not in visited_vertexes[ant_id]:
                # get pheromone level for neighbor vertex
                ph_level = get_pheromone_level_for_edge(start_v, neighbor, edges)
                if current_highest_ph > ph_level:
                    current_highest_ph = ph_level
                    current_best_neighbor = neighbor
                elif current_highest_ph == ph_level:
                    if random() > theta:
                        current_best_neighbor = neighbor
                        
        # spreading pheromones on selected edge
        # update coefficient for pheromone level on an edge
        update_coefficient = 1
        spread_pheromones(start_v, neighbor, edges, update_coefficient)
        vaporization(edges, vaporization_rate)
    return current_best_neighbor
    
def vaporization(edges, vaporization_rate):
    for i in range(len(edges)):
        prev_ph = edges[i]["ph"]
        new_ph = prev_ph * vaporization_rate
        edges[i]["ph"] = new_ph
    return edges
    
def spread_pheromones(start_v, end_v, edges, update_coefficient):
    for edge in edges:
        if edge["st_v"] == start_v and edge["end_v"] == end_v:
            prev_ph = edge["ph"]
            new_ph = prev_ph * update_coefficient
            edge["ph"] = new_ph
                                    
def get_pheromone_level_for_edge(start_v, end_v, edges):
    for edge in edges:
        if edge["st_v"] == start_v and edge["end_v"] == end_v:
            return edge["ph"]

def find_neighbors(vertex):
    global distances_df
    neighbors = []
    neighbors_names = list(distances_df.columns)[:-1]
    neighbors_distances = list(distances_df[vertex].to_numpy())
    for i in range(len(neighbors_distances)):
        if neighbors_distances[i] > 0:
            neighbors.append(neighbors_names[i])
    return(neighbors)

def get_path(visited_vertexes, m):
    path = visited_vertexes[m]
    return path

# TEST EXAMPLE
distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
capacities_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/capacities_df.pkl"
costs_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/costs_df.pkl"

distances_df = load_df(distances_df_pkl)
demands_df = load_df(demands_df_pkl)
capacities_df = load_df(capacities_df_pkl)
costs_df = load_df(costs_df_pkl)
vertices = list(distances_df.columns)[:-1]

start_vertex = "Freiburg"
end_vertex = "Oldenburg"
ant_colony_size = 10
ph_init = 0
vapor_rate = 0.9
theta = 0.8

path = aco(start_vertex, end_vertex, vertices, ant_colony_size, ph_init, vapor_rate, theta)
print(path)