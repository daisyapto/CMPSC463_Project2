import geopandas as gpd
import pickle
from Algorithms.Graph import Graph
from Algorithms.Snap_Centers import snap_to_nearest
from shapely.geometry import Point

# Load evac centers
evac_centers = gpd.read_file(
    "Data/Processed Data/Facilities.geojson"
)
evac = evac_centers.to_crs(epsg=4326)

# Load hazard graph
G = Graph()
with open("../Data/hazard_graph.pkl", "rb") as f:
    loaded_graph = pickle.load(f)

if loaded_graph:
    G.graph = loaded_graph

snapped_centers = {}
for center in evac.geometry:
    lon, lat = center.x, center.y
    snapped = snap_to_nearest(G.graph, Point(lon, lat))
    snapped_centers[(lon, lat)] = snapped

# Save mapping
with open("Data/evac_snapped.pkl", "wb") as f:
    pickle.dump(snapped_centers, f)
