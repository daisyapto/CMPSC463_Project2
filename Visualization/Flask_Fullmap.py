import folium, os
import geopandas as gpd
from folium import GeoJson
from folium.plugins import AntPath
from Visualization.MST import draw_mst_layer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "processed")


def draw_flask_full_map(user_node, routes, mst_edges):
    # ========== Load Data ==========
    roads = gpd.read_file(os.path.join(DATA_DIR, "Street_Centerline.geojson")).to_crs(4326)
    floods = gpd.read_file(os.path.join(DATA_DIR, "Floods.geojson")).to_crs(4326)
    evac = gpd.read_file(os.path.join(DATA_DIR, "Facilities.geojson")).to_crs(4326)

    roads = roads[["geometry"]]
    floods = floods[["geometry"]]

    # ========== Setup Map ==========
    bounds = roads.total_bounds
    center_lon = (bounds[0] + bounds[2]) / 2
    center_lat = (bounds[1] + bounds[3]) / 2

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # ========== Base Layers ==========

    GeoJson(
        roads,
        name="Roads",
        style_function=lambda x: {
            "color": "blue",
            "weight": 1.5,
            "opacity": 0.7
        }
    ).add_to(m)

    GeoJson(
        floods,
        name="Flood Zones",
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 1,
            "fillOpacity": 0.3
        }
    ).add_to(m)

    # ========== Evacuation Centers Layer ==========
    evac_layer = folium.FeatureGroup(name="Evacuation Centers")

    for pt in evac.geometry:
        folium.Marker(
            [pt.y, pt.x],
            popup="Evac Center",
            icon=folium.Icon(color="purple")
        ).add_to(evac_layer)

    evac_layer.add_to(m)

    # ========== User Point ==========
    folium.Marker(
        [user_node.y, user_node.x],
        popup="User Location",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

    # ========== Draw Routes Animations ==========
    route_layer = folium.FeatureGroup(name="Evac Routes")

    colors = ["lime", "orange", "purple", "black", "darkred", "pink", "cyan"]

    for idx, (evac_node, dist, path) in enumerate(routes):
        color = colors[idx % len(colors)]
        coords = [(lat, lon) for (lon, lat) in path]

        AntPath(
            locations=coords,
            delay=700,
            dash_array=[10, 20],
            weight=5,
            color=color,
            pulse_color="white",
            opacity=0.9,
            popup=f"Evac #{idx + 1} | Distance: {dist:.3f}"
        ).add_to(route_layer)

    route_layer.add_to(m)

    # ========== Evac MST ==========
    draw_mst_layer(m, mst_edges)

    folium.LayerControl(collapsed=False).add_to(m)
    return m._repr_html_()
