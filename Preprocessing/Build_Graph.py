from Algorithms.Graph import Graph
from shapely.geometry import LineString
import geopandas as gpd
from shapely.ops import unary_union
from math import hypot

roads = gpd.read_file("Data/Processed Data/Street_Centerline.geojson")
floods = gpd.read_file("Data/Processed Data/Floods.geojson")
hurricanes = gpd.read_file("Data/Processed Data/Hurricanes.geojson")
evac_centers = gpd.read_file("Data/Processed Data/Facilities.geojson")

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

# Load graph into a pickle file
# with open("Data/Pickle/hazard_graph.pkl", "wb") as f:
#     pickle.dump(G.graph, f, protocol=pickle.HIGHEST_PROTOCOL)
