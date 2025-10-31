import geopandas as gpd  # Read in geojson files
from Algorithms.Graph import build_graph
import pickle
from pathlib import Path

# ===== Read in Data =====
# to_crs with 26918 converts values to meters

# Get the directory where this script is located
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent  # Go up two levels to Project 2

# Define paths relative to project root
raw_data_dir = project_root / "Data" / "Raw"
output_dir = project_root / "Data"

print("Reading road data")
roads = gpd.read_file(str(raw_data_dir / "philadelphia_roads.geojson")).to_crs(26918)

print("Reading flood data")
flood_zones = gpd.read_file(str(raw_data_dir / "philadelphia_flood_zone.geojson")).to_crs(26918)
flood_zones = flood_zones[["fld_zone", "floodway", "depth", "geometry"]]

print("Reading hurricane data")
hurricane_track = gpd.read_file(str(raw_data_dir / "philadelphia_hurricane_track.geojson")).to_crs(26918)

print("Reading evac center data")
evacuation_centers = gpd.read_file(str(raw_data_dir / "philadelphia_evacuation_centers.geojson")).to_crs(26918)

print("Building graph")

# Build graph
evacuation_graph = build_graph(roads, flood_zones, hurricane_track, evacuation_centers)

# Save graph to a pickle file
with open(str(output_dir / "evacuation_graph.pkl"), "wb") as f:
    pickle.dump(evacuation_graph, f)
