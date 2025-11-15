import geopandas as gpd

"""
Reduce large size of road map files
"""

# Read in road data
roads = gpd.read_file("/Users/andrewherman/CMP463/Project 2/Data/Raw/philadelphia_roads.geojson")
roads = roads.set_crs(4326).to_crs(26918)

roads["geometry"] = roads["geometry"].simplify(
    tolerance=5,
    preserve_topology=True
)

# # Write back to geojson
roads.to_file("/Users/andrewherman/CMP463/Project 2/Data/Raw/philadelphia_roads.geojson", driver="GeoJSON")
