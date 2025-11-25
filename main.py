import geopandas as gpd
from shapely.geometry import Point
from Algorithms.Graph import Graph
from shapely.ops import unary_union
import random
from Visualization.mapFoliium import draw_route
import pickle

roads = gpd.read_file("")
floods = gpd.read_file("")
hurricanes = gpd.read_file("")
evac_centers = gpd.read_file("")

roads = roads.to_crs(epsg=4326)
floods = floods.to_crs(epsg=4326)
evac = evac_centers.to_crs(epsg=4326)

flood_union = unary_union(floods.geometry)
hurricane_union = unary_union(hurricanes.geometry)

G = Graph()
with open("hazard_graph.pkl", "rb") as f:
    loaded_graph = pickle.load(f)

if loaded_graph:
    G.graph = loaded_graph

lat = float(input("Enter your latitude coordinate: "))
lon = float(input("Enter your longitude coordinate: "))
# user_pos = Point(39.95, -75.16)  # lat, lon = y,x
user_pos = Point(lat, lon)  # lat, lon = y,x
distances, previous = G.dijkstra(user_pos)
#print(previous)

"""
temp_all_paths = []
for center in evac.geometry:
    goal = (center.x, center.y)
    path = G.get_path(previous, goal)
    print(path)
    temp_all_paths.append(path)
"""

random_evac = random.choice(evac.geometry)
path = G.get_path(previous, (random_evac.x, random_evac.y))
print("Path", path)

##### Uncomment the following lines to test Prim's ######

test = Point(-75.21306878970346, 40.02152944119314)
lastPrim = Point(-75.20932498164714, 40.07782488785368)
test1 = (test.x, test.y)
prim = G.primMST(evac.geometry, test1)
order = []
for item in prim[0]:
    order.append(item[1])
# Debug statements
print(len(order))
print(type(order[0]))
print(len(path))
print(type(path[0]))
print(len(evac.geometry))

# Added to draw_route function parameter for the order of the nodes for Prim's but it is 190,000+ node visits since its MST, not path
# Doesn't load into HTML evac_map2.html
# Unsure how to fix
draw_route(user_pos, random_evac, path, order)
