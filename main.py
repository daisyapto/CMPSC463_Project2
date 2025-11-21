"""
Testing reading in data
"""

import geopandas as gpd
from shapely.geometry import LineString, Point
from Algorithms.Graph import Graph
from math import hypot
from shapely.ops import unary_union

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

for idx, road in roads.iterrows():
    line: LineString = road.geometry
    coords = list(line.coords)

    for i in range(len(coords) - 1):
        x1, y1 = coords[i][1], coords[i][0]
        x2, y2 = coords[i + 1][1], coords[i + 1][0]

        risk_factor = 1

        if line.intersects(flood_union):
            risk_factor += 1
        if line.intersects(hurricane_union):
            risk_factor += 1.5

        weight = hypot(x2 - x1, y2 - y1) * risk_factor

        G.add_edge((y1, x1), (y2, x2), weight)

# for node in G.graph.keys():
#     if not isinstance(node, tuple) or len(node) != 2 or not all(isinstance(x, (int, float)) for x in node):
#         print(f"Node {node} is not a valid coordinate pair.")
#         continue
#     print("Nah we good")
