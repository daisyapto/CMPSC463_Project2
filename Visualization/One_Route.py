import folium, os
import geopandas as gpd
from folium import GeoJson

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "processed")


def draw_route(user_node, evac_node, path, prim_nodes):
    roads = gpd.read_file(os.path.join(DATA_DIR, "Street_Centerline.geojson"))
    roads = roads.to_crs(epsg=4326)
    roads.geometry = roads.geometry.apply(lambda g: g)

    floods = gpd.read_file(os.path.join(DATA_DIR, "Floods.geojson"))

    evac = gpd.read_file(os.path.join(DATA_DIR, "Facilities.geojson"))
    evac = evac.to_crs(epsg=4326)

    # Find center of map
    center_lat = roads.geometry.bounds[['miny', 'maxy']].mean().mean()
    center_lon = roads.geometry.bounds[['minx', 'maxx']].mean().mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Draw Roads
    GeoJson(
        roads,
        name="Roads",
        style_function=lambda x: {"color": "blue", "weight": 2, "opacity": 0.7},
    ).add_to(m)

    # Draw Floods
    GeoJson(
        floods,
        name="Flood Zones",
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 1,
            "fillOpacity": 0.3,
        },
    ).add_to(m)

    # Draw User Location
    folium.Marker(
        location=[user_node.x, user_node.y],
        popup="User Start Location",
        icon=folium.Icon(color="blue", icon="user"),
    ).add_to(m)

    # Draw route polyline
    folium.PolyLine(
        locations=[(lat, lon) for (lon, lat) in path],
        weight=5,
        opacity=0.8,
        color="green",
    ).add_to(m)

    # Add marker for that evac center
    folium.Marker(
        location=[evac_node.y, evac_node.x],
        popup="Evacuation Center",
        icon=folium.Icon(color="green", icon="info-sign"),
    ).add_to(m)
    # popup=f"Evac Center<br>Distance = {distances:.2f}",

    # New addition for prim node line, unsure how to map Prim since so many node visits
    folium.PolyLine(
        locations=[(lat, lon) for (lon, lat) in prim_nodes], color='blue', weight=2, opacity=0.8
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save("evac_map2.html")
