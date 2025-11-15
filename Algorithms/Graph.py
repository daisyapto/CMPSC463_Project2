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


def build_graph(roads, flood_zones, hurricane_track):
    G = Graph()

    flood_union = flood_zones.unary_union
    hurricane_union = hurricane_track.buffer(50).unary_union

    for _, row in roads.iterrows():
        coords = list(row.geometry.coords)

        for i in range(len(coords) - 1):
            # Get longitude and latitude of each coordinate
            ax, ay = coords[i][0], coords[i][1]
            bx, by = coords[i + 1][0], coords[i + 1][1]

            a = (ax, ay)
            b = (bx, by)

            # String that connects the two points
            line = LineString([a, b])

            # Distance in meters
            distance = np.linalg.norm(np.array(a) - np.array(b))

            # Multiplier on risk levels based on hurricane, flood, and evac center distance
            risk_factor = 1

            # Road intersections with flood zones
            if flood_union.intersects(line):
                risk_factor += 1.5

            # Road intersections with hurricane track
            if hurricane_union.intersects(line):
                risk_factor += 1.0

            weight = distance * risk_factor

            G.add_edge(a, b, weight)
    return G
