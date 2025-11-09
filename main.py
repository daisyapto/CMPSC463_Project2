import pickle
import os
import geopandas as gpd
from Visualization.Roadmap import roadmap_visualization, roadmap_evacuation_centers
from Algorithms.Dijkstra import dijkstra

evacuation_centers = gpd.read_file(
    "/Users/andrewherman/CMP463/Project 2/Data/Raw/philadelphia_evacuation_centers.geojson")

if os.path.exists("/Users/andrewherman/CMP463/Project 2/Data/evacuation_graph.pkl"):
    with open("/Users/andrewherman/CMP463/Project 2/Data/evacuation_graph.pkl", "rb") as f:
        G = pickle.load(f)

if G:
    # roadmap_evacuation_centers(G.graph, evacuation_centers)
    for u in G.graph:
        for v, w in G.graph[u]:
            u1, u2 = round(u[0], 2), round(u[1], 2)
            v1, v2 = round(v[0], 2), round(v[1], 2)

            print(f"{u1, u2} --> {v1, v2} : {round(w, 2)}")
#     roadmap_visualization(G.graph)
#     dijkstra(G.graph, (39.95, -75.16))
