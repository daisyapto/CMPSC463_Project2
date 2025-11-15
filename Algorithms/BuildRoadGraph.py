import geopandas as gpd
from Algorithms.Graph import build_graph
import pickle
from pathlib import Path

# Path Setup to read in data
script_dir = Path(__file__).parent
project_root = script_dir.parent
raw_data_dir = project_root / "Data" / "Raw"
output_dir = project_root / "Data" / "Processed"

print("Reading road data")
roads = gpd.read_file(raw_data_dir / "philadelphia_roads.geojson")

print("Reading flood data")
flood_zones = gpd.read_file(raw_data_dir / "philadelphia_flood_zone.geojson")
flood_zones = flood_zones[["fld_zone", "floodway", "depth", "geometry"]]

print("Reading hurricane data")
hurricane_track = gpd.read_file(raw_data_dir / "philadelphia_hurricane_track.geojson")

# ===== Convert to meters =====
flood_zones = flood_zones.set_crs(4326).to_crs(26918)
hurricane_track = hurricane_track.set_crs(4326).to_crs(26918)
roads = roads.to_crs(26918)

# Confirm CRS metric is the same for all three datasets
print("Roads CRS:", roads.crs)
print("Flood CRS:", flood_zones.crs)
print("Hurricane CRS:", hurricane_track.crs)

# Build graph
print("Building graph...")
G = build_graph(roads, flood_zones, hurricane_track)

# save graph as pickle
output_path = output_dir / "evacuation_graph.pkl"
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "wb") as f:
    pickle.dump(G, f)

print("Graph saved to:", output_path)
