import folium
from Algorithms.Dijkstra import define_starting_vertex


def roadmap_visualization(graph):
    m = folium.Map(location=[39.95, -75.16], zoom_start=12)

    for u in graph:
        for v, w in graph[u]:
            folium.PolyLine([u, v], color="blue", weight=2, opacity=0.6).add_to(m)

    m.save("Visualization/road_graph.html")


def roadmap_evacuation_centers(graph, evac_centers):
    # Map starting point
    m = folium.Map(location=[39.95, -75.16], zoom_start=12)

    # Add evacuation centers to map
    for i, row, in evac_centers.iterrows():
        coords = list(row.geometry.coords)
        lat, lon = coords[0][1], coords[0][0]
        closest_vertex = define_starting_vertex(graph, (lat, lon))
        folium.Marker([closest_vertex, lon], popup="Shelter", icon=folium.Icon(color="green")).add_to(m)

    # Save to file
    m.save("Visualization/road_graph.html")
