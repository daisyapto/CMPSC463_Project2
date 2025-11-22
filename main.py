import geopandas as gpd
from shapely.geometry import Point
from Algorithms.Graph import Graph
from shapely.ops import unary_union
import random
from Visualization.mapFoliium import draw_route
import pickle

roads = gpd.read_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Street_Centerline.geojson")
floods = gpd.read_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Floods.geojson")
hurricanes = gpd.read_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Hurricanes.geojson")
evac_centers = gpd.read_file("/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Facilities.geojson")

roads = roads.to_crs(epsg=4326)
floods = floods.to_crs(epsg=4326)
evac = evac_centers.to_crs(epsg=4326)

flood_union = unary_union(floods.geometry)
hurricane_union = unary_union(hurricanes.geometry)

G = Graph()
with open("Data/hazard_graph.pkl", "rb") as f:
    loaded_graph = pickle.load(f)

if loaded_graph:
    G.graph = loaded_graph


user_pos = Point(39.95, -75.16)  # lat, lon = y,x
distances, previous = G.dijkstra(user_pos)
print(distances)

# temp_all_paths = []
# for center in evac.geometry:
#     goal = (center.x, center.y)
#     path = G.get_path(previous, goal)
#     print(path)
#     temp_all_paths.append(path)


#
# random_evac = random.choice(evac.geometry)
# path = G.get_path(previous, (random_evac.x, random_evac.y))
# draw_route(user_pos, random_evac, path)
