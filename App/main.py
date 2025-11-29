from flask import Flask

app = Flask(__name__)
"""
import random, pickle
from shapely.geometry import Point
from Visualization.Full_Map import draw_full_map
from Algorithms.K_Nearest import k_nearest_evacuation_centers
from Algorithms.Prims import prim_mst

with open("../Data/Pickle/hazard_graph.pkl", "rb") as f:
    graph = pickle.load(f)

with open("../Data/Pickle/evac_kdtree.pkl", "rb") as f:
    tree, evacuation_coords, snapped_centers = pickle.load(f)

center_city = (-75.1575, 39.9509)
source = Point(center_city[0], center_city[1])

# Random source
# random_lat = random.uniform(39.95, 40.04)
# random_lon = random.uniform(-75.05, -75.00)
# source = Point(random_lon, random_lat)


# K nearerst evacuation centers
K = 8
routes = k_nearest_evacuation_centers(graph, source, snapped_centers, K, tree)

# Get MST edges
mst_edges = prim_mst(evacuation_coords)

draw_full_map(source, routes, mst_edges, save_file="../ui/full_map_merge_test3.html")
"""