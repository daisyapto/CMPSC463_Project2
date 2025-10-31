import requests, json

query = """
[out:json][timeout:25];
node["amenity"="shelter"](39.87,-75.28,40.14,-74.95);
out body;
"""
r = requests.get("https://overpass-api.de/api/interpreter", params={"data": query})
shelters = r.json()
with open("/Users/andrewherman/CMP463/Project 2/Data/Raw/philadelphia_evacuation_centers.json", "w") as f:
    json.dump(shelters, f)
