import heapq
import math
import sys
from shapely.geometry import Point
import pickle


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def get_neighbors(self, node):
        return self.graph.get(node, []).items()

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def dijkstra(self, source):
        if source not in self.graph:
            source = self.snap_to_nearest(source)

        # Initialize the priority queue with the source node
        priority_queue = [(0, source)]  # (distance, vertex)

        # Distances dictionary to store the shortest path lengths
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[source] = 0

        previous = {vertex: None for vertex in self.graph}

        explored = set()

        while priority_queue:
            # Extract the vertex with the smallest distance from the priority queue
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # If the vertex is already explored, skip it
            if current_distance > distances[current_vertex]:
                continue

            explored.add(current_vertex)

            # Update distances for neighbors of the current vertex
            for neighbor, weight in self.graph[current_vertex].items():
                if neighbor in explored:
                    continue

                new_dist = current_distance + weight  # Current total weight to node

                if new_dist < distances[neighbor]:  # shorter path to neighbor found
                    distances[neighbor] = new_dist  # update distance
                    previous[neighbor] = current_vertex  # update previous node
                    heapq.heappush(priority_queue, (new_dist, neighbor))  # update priority queue

        filtered_distances = {k: w for k, w in distances.items() if w < 0.2}
        return filtered_distances, previous

    def get_path(self, previous, goal):
        if goal not in self.graph:
            print(f"Snapping {goal} to nearest node...")
            goal = self.snap_to_nearest(Point(goal[1], goal[0]))
            print(f"\t{goal}")

        # reconstruct path
        path = []
        node = goal
        visited_path = set()
        while node is not None:
            if node in visited_path:
                print("Cycle detected.")
                break
            visited_path.add(node)
            path.append(node)
            node = previous[node]
        path.reverse()
        return path

    def inside_philly(self, lat, lon):
        return (
                39.86 <= lat <= 40.14 and
                -75.30 <= lon <= -74.96
        )

    # Pass source as a Point(y,x)
    def snap_to_nearest(self, source):
        # Not a point
        if not isinstance(source, Point):
            raise TypeError("Source must be a shapely Point object.")

        # verify near philly
        if not self.inside_philly(lon=source.y, lat=source.x):
            print("Source is outside Philadelphia.")
            return None

        return min(
            self.graph.keys(),
            key=lambda n: Point(n[1], n[0]).distance(source))

    def get_k_nearest_paths(self, k):
        pass

    def __str__(self):
        return f"GRAPH DETAILS\nKeys: {len(self.graph.keys())}"

    # Reference: https://www.geeksforgeeks.org/dsa/prims-minimum-spanning-tree-mst-greedy-algo-5/
    def primMST(self, evac, source):
        ################### Building adjacency matrix from Facilities ##################
        evacCenters = len(evac)
        matrixForPrim = [[0 for _ in range(evacCenters)] for _ in range(evacCenters)]

        coords_Evac_Centers = []
        for item in evac:
            coords_Evac_Centers.append((item.x, item.y))
        # print(coords_Evac_Centers)
        matrix = [[0 for _ in range(len(coords_Evac_Centers))] for _ in range(len(coords_Evac_Centers))]

        for i in range(len(coords_Evac_Centers)):
            for j in range(len(coords_Evac_Centers)):
                matrix[i][j] = self.distance(coords_Evac_Centers[i], coords_Evac_Centers[j])
        # print(matrix)

        visited = [False] * len(coords_Evac_Centers)
        weight = 0
        tree = []
        # Initialize the priority queue with the source node
        priority_queue = [(0, source)]  # (distance, vertex)

        while priority_queue:
            dist, vertex = heapq.heappop(priority_queue)
            vertexIndex = coords_Evac_Centers.index(vertex)
            if visited[vertexIndex]:
                continue
            weight += dist
            visited[vertexIndex] = True

            for connection in matrix[vertexIndex]:
                if connection == 0:
                    continue
                if not visited[matrix[vertexIndex].index(connection)]:
                    heapq.heappush(priority_queue, (connection, coords_Evac_Centers[matrix[vertexIndex].index(connection)]))
                    tree.append((coords_Evac_Centers[vertexIndex], coords_Evac_Centers[matrix[vertexIndex].index(connection)], weight))

        return tree, weight