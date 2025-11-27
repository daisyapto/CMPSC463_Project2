import folium, os
import geopandas as gpd
from folium import GeoJson

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "processed")


def draw_k_routes(user_node, k_paths):
    # Load base layers
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

    # Base layers
    GeoJson(
        roads,
        name="Roads",
        style_function=lambda x: {"color": "blue", "weight": 2, "opacity": 0.7},
    ).add_to(m)

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

    # User marker
    folium.Marker(
        location=[user_node.y, user_node.x],  # (lat, lon)
        popup="User Location",
        icon=folium.Icon(color="blue", icon="user"),
    ).add_to(m)

    # Route colors
    route_colors = ["green", "orange", "purple", "black", "darkred"]

    # Draw each route
    for route_index, (evac_idx, snapped_node, dist, path) in enumerate(k_paths):
        color = route_colors[route_index % len(route_colors)]

        # Path nodes (lon, lat) → (lat, lon)
        route_coords = [(lat, lon) for (lon, lat) in path]

        folium.PolyLine(
            locations=route_coords,
            weight=5,
            opacity=0.8,
            color=color,
        ).add_to(m)

        # Evac marker (snapped_node = (lon, lat))
        folium.Marker(
            location=[snapped_node[1], snapped_node[0]],  # (lat, lon)
            popup=f"Evac Center #{route_index + 1}<br>Distance: {dist:.4f}",
            icon=folium.Icon(color="green", icon="info-sign"),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save("ui/evac_map_k.html")
