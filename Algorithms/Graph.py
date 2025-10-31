import numpy as np
from shapely.geometry import LineString


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        # If vertex not in graph yet
        if u not in self.graph:
            self.graph[u] = [(v, weight)]
        else:
            # Append to existing vertex
            self.graph[u].append((v, weight))

        # Same for v since undirected
        if v not in self.graph:
            # If vertex not in graph yet
            self.graph[v] = [(u, weight)]
        else:
            # Append to existing vertex
            self.graph[v].append((u, weight))

    def neighbors(self, node):
        # Node is in graph return its neighboring nodes with weights
        if node in self.graph:
            return self.graph[node]

        print("Node not in graph")
        return None


def build_graph(roads, flood_zones, hurricane_track, evacuation_centers):
    G = Graph()

    for _, row in roads.iterrows():
        coords = list(row.geometry.coords)
        for i in range(len(coords) - 1):
            a, b = coords[i], coords[i + 1]
            distance = np.linalg.norm(np.array(a) - np.array(b))
            line = LineString([a, b])

            # Multiplier on risk levels based on hurricane, flood, and evac center distance
            risk_factor = 1

            # Risk of Flood
            if flood_zones.intersects(line).any():
                risk_factor += 1.5

            if hurricane_track.buffer(0.02).intersects(line).any():
                risk_factor += 1.0

            weight = distance * risk_factor

            G.add_edge(a, b, weight)
    return G.graph
