import heapq
from shapely.geometry import Point


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

    def dijkstra(self, start, goal):
        # Initialize the priority queue with the source node
        priority_queue = [(0, start)]  # (distance, vertex)

        # Distances dictionary to store the shortest path lengths
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0

        previous = {vertex: None for vertex in self.graph}

        while priority_queue:
            # Extract the vertex with the smallest distance from the priority queue
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_vertex == goal:
                break

            # If the vertex is already explored, skip it
            if current_distance > distances[current_vertex]:
                continue

            # Update distances for neighbors of the current vertex
            for neighbor, weight in self.graph[current_vertex]:
                new_dist = current_distance + weight  # Current total weight to node
                if new_dist < distances[neighbor] or neighbor not in distances:  # shorter path to neighbor found
                    distances[neighbor] = new_dist  # update distance
                    previous[neighbor] = current_vertex  # update previous node
                    heapq.heappush(priority_queue, (new_dist, neighbor))  # update priority queue

        if goal not in distances:
            return float('inf'), None

        # reconstruct path
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()

        return distances[goal], path

    # Pass source as a Point(y,x)
    def snap_to_nearest(self, source):
        if not isinstance(source, Point):
            raise TypeError("Source must be a shapely Point object.")

        return min(
            self.graph.keys(),
            key=lambda n: Point(n[1], n[0]).distance(source))

    def __str__(self):
        return f"GRAPH DETAILS\nKeys: {len(self.graph.keys())}"
