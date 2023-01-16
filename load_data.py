import pandas as pd
from import_data import load_df
distances_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/distances_df.pkl"
demands_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/demands_df.pkl"
capacities_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/capacities_df.pkl"
costs_df_pkl = "/Users/maciekswiech/Desktop/PW/Sem7/POP/projekt/dane/costs_df.pkl"

distances_df = load_df(distances_df_pkl)
demands_df = load_df(demands_df_pkl)
capacities_df = load_df(capacities_df_pkl)
costs_df = load_df(costs_df_pkl)