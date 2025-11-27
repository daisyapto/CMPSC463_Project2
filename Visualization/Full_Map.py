import folium, os
import geopandas as gpd
from folium import GeoJson
from Visualization.MST import draw_mst_layer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "processed")


def draw_full_map(user_node, routes, mst_edges, save_file="ui/full_evac_map.html"):
    roads = gpd.read_file(os.path.join(DATA_DIR, "Street_Centerline.geojson"))
    roads = roads.to_crs(epsg=4326)
    roads.geometry = roads.geometry.apply(lambda g: g)

    floods = gpd.read_file(os.path.join(DATA_DIR, "Floods.geojson"))

    evac = gpd.read_file(os.path.join(DATA_DIR, "Facilities.geojson"))
    evac = evac.to_crs(epsg=4326)

    roads = roads[["geometry"]].copy()
    floods = floods[["geometry"]].copy()
    evac = evac[["geometry"]].copy()

    # Map center
    center_lat = roads.geometry.bounds[['miny', 'maxy']].mean().mean()
    center_lon = roads.geometry.bounds[['minx', 'maxx']].mean().mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Roads layer
    GeoJson(
        roads.__geo_interface__,
        name="Roads",
        style_function=lambda x: {"color": "blue", "weight": 2}
    ).add_to(m)

    # Flood zones
    GeoJson(
        floods.__geo_interface__,
        name="Flood Zones",
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 1,
            "fillOpacity": 0.3,
        },
    ).add_to(m)

    # Evacuation Center Markers Layer
    evac_layer = folium.FeatureGroup(name="Evacuation Centers")

    for pt in evac.geometry:
        lon, lat = pt.x, pt.y
        folium.Marker(
            location=[lat, lon],
            popup=f"Evac Center<br>({lat:.4f}, {lon:.4f})",
            icon=folium.Icon(color="purple", icon="info-sign")
        ).add_to(evac_layer)

    evac_layer.add_to(m)

    # User location
    folium.Marker(
        location=[user_node.y, user_node.x],
        popup="User Location",
        icon=folium.Icon(color="blue", icon="user"),
    ).add_to(m)

    # MST layer
    draw_mst_layer(m, mst_edges)

    # K shortest paths
    colors = ["green", "orange", "purple", "black", "brown"]

    for idx, (evac_node, dist, path) in enumerate(routes):
        color = colors[idx % len(colors)]

        path_coords = [(lat, lon) for (lon, lat) in path]

        folium.PolyLine(
            locations=path_coords,
            color=color,
            weight=5,
            opacity=0.8,
            popup=f"Route to evac #{idx + 1}\nDistance={dist:.3f}",
        ).add_to(m)

        folium.Marker(
            location=[evac_node[1], evac_node[0]],
            popup=f"Evac #{idx + 1}",
            icon=folium.Icon(color="green", icon="info-sign"),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(save_file)
