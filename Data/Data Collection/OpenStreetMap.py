"""
Road networks by city or region
"""

import requests
import json

query = """
[out:json][timeout:25];
area["wikidata"="Q1345"]->.a;
(
  way["highway"](area.a);
);
out geom;
"""
url = "https://overpass-api.de/api/interpreter"
r = requests.get(url, params={"data": query})
roads_json = r.json()

features = []
for element in roads_json["elements"]:
    if 'geometry' in element:
        coords = [(pt["lon"], pt["lat"]) for pt in element["geometry"]]
        features.append({"type": "Feature",
                         "geometry": {"type": "LineString", "coordinates": coords},
                         "properties": element.get("tags", {})})

geojson = {"type": "FeatureCollection", "features": features}

with open("/Users/andrewherman/CMP463/Project 2/Data/Raw/philadelphia_roads.geojson", "w") as f:
    json.dump(geojson, f, indent=2)
