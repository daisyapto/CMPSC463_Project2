import pickle
import os

import geopandas as gpd
from Visualization.Roadmap import roadmap_visualization, roadmap_evacuation_centers, draw_route
from Algorithms.Dijkstra import dijkstra, find_nearest_evacuation_center, get_nearest_vertex

evacuation_centers = gpd.read_file(
    "/Users/andrewherman/CMP463/Project 2/Data/Raw/philadelphia_evacuation_centers.geojson").to_crs(26918)


graph_path = "/Users/andrewherman/CMP463/Project 2/Data/Processed/evacuation_graph.pkl"
if os.path.exists(graph_path):
    with open(graph_path, "rb") as f:
        G = pickle.load(f)

if G:
    graph = G.graph
    close_centers = []
    threshold = 250 #meters

    for geom in evacuation_centers.geometry:
        center = (geom.x, geom.y)
        vertex, distance = get_nearest_vertex(graph, center)

        if distance < threshold:
            close_centers.append([center, vertex, distance])

    for center, snapped, dist in close_centers:
        print(f"Center {center} -> snapped to {snapped}, dist = {dist:.2f} m")