from folium import GeoJson


def draw_mst_layer(map_obj, mst_edges):
    mst_features = []

    for (lon1, lat1), (lon2, lat2) in mst_edges:
        mst_features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [lon1, lat1],
                    [lon2, lat2]
                ]
            },
            "properties": {}
        })

    mst_geojson = {
        "type": "FeatureCollection",
        "features": mst_features
    }

    GeoJson(
        mst_geojson,
        name="Evac MST",
        style_function=lambda x: {
            "color": "darkred",
            "weight": 3,
            "opacity": 0.8
        }
    ).add_to(map_obj)
