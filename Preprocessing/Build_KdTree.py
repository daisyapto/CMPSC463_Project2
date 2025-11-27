import geopandas as gpd
import pickle
from Algorithms.Graph import Graph
from shapely.geometry import Point
from scipy.spatial import KDTree
from Algorithms.Snap_Centers import snap_to_nearest

# Load evac centers
evac_centers = gpd.read_file(
    "/Users/andrewherman/CMP463/SafetyGPS/Data/Processed Data/Facilities.geojson"
).to_crs(epsg=4326)

# Build coordinate list (lon, lat)
evac_coords = [(pt.x, pt.y) for pt in evac_centers.geometry]

# Build KDTree
tree = KDTree(evac_coords)

# Load your road Pickle
G = Graph()
with open("../Data/hazard_graph.pkl", "rb") as f:
    loaded = pickle.load(f)
    G.graph = loaded

# Snap each evac center ONCE and store by index
snapped_centers = {}

for i, (lon, lat) in enumerate(evac_coords):
    snapped_node = snap_to_nearest(G.graph, Point(lon, lat))
    snapped_centers[i] = snapped_node

# Save KDTree + coords + snapped mapping
with open("Data/evac_kdtree.pkl", "wb") as f:
    pickle.dump((tree, evac_coords, snapped_centers), f)
