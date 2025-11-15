import numpy as np
import pickle, heapq
import sys
from shapely.geometry import LineString

class Graph:
    def __init__(self, vertices):
        self.graph = {}
        self.V = vertices

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

    def define_starting_vertex(self, user_position):
        return min(self.graph.keys(), key=lambda x: np.linalg.norm(np.array(x) - np.array(user_position)))

    # Reference: CMPSC 463 Google Colab Notebook 9
    def dijkstra(self, source):
        # Initialize the priority queue with the source node
        priority_queue = [(0, source)]  # (distance, vertex)

        # Distances dictionary to store the shortest path lengths
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[source] = 0

        # Initialize the set of explored nodes
        explored = set()

        while priority_queue:
            # Extract the vertex with the smallest distance from the priority queue
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # If the vertex is already explored, skip it
            if current_vertex in explored:
                continue

            # Mark the vertex as explored
            explored.add(current_vertex)

            # Update distances for neighbors of the current vertex
            for i in range(len(self.graph[current_vertex])):
                neighbor = self.graph[current_vertex][i][0]
                weight = self.graph[current_vertex][i][1]
                distance = current_distance + weight

                # If a shorter path to the neighbor is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

    def connections(self, source):
        print(f"Connections for source: {source}:")
        distances = self.dijkstra(source)
        connections = {}
        for item in distances:
            if distances[item] != float('infinity'):
                connections[item] = distances[item]

        return connections

    # Reference: Colab Notebook 12
    # A utility function to print the constructed MST stored in parent[]
    def printMST(self, parent):
        total = 0
        print("Edge \tWeight")
        for i in range(1, self.V):
            print(parent[i], "-", i, "\t", self.graph[i][parent[i]])
            total += self.graph[i][parent[i]]
        print(f"Total: {total}")

    # A utility function to find the vertex with minimum distance value,
    # from the set of vertices not yet included in shortest path tree
    def minKey(self, key, mstSet):

        # Initialize min value as very large value
        currMin = sys.maxsize  # the largest value, 2^63-1
        min_key = None

        for point in self.graph:  # choose a node having a min key
            for v in self.graph[point]:
                if key[v[0]] < currMin and mstSet[v[0]]== False:  # vertex in V-X
                    currMin = key[v[0]]
                    min_key= v[0]

        return min_key

    def primMST(self):

        # Initialization, self.V = number of vertices
        key = {point: sys.maxsize for point in self.graph}  # Key values used to pick minimum weight edge in cut
        parent = {point: None for point in self.graph}  # Array to store constructed MST
        key[0] = 0  # Make key 0 so that this vertex is picked as first vertex
        mstSet = {point: False for point in self.graph}  # if True, it is in X, if not, it is in V-X

        parent[0] = -1  # First node is always the root

        for point in self.graph:

            # Pick the minimum distance vertex from the set of vertices not yet processed
            u = self.minKey(key, mstSet)

            # Put the minimum distance vertex in the shortest path tree
            mstSet[u] = True

            # Update dist value of the adjacent vertices of the picked vertex only if the current
            # distance is greater than new distance and the vertex in not in the shortest path tree
            for v in self.graph[point]:

                # graph[u][v] is non zero only for adjacent vertices of m
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if 0 < self.graph[point][self.graph[point].index(v)][1] < key[v[0]] and mstSet[v[0]] == False:
                    key[v[0]] = self.graph[point][self.graph[point].index(v)][1]
                    parent[v[0]] = u

        self.printMST(parent)

# Used in BuildEvacuationGraph.py
def build_graph(roads, flood_zones, hurricane_track):
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
    return G


##################################
# Test cases with points; many inf because many points unconnected
# Graph item structure = (x1, y1) : [(x2, y2), weight]
file = "<add path here>"
with open(file, "rb") as f:
    evacuation_graph = pickle.load(f)
graph = Graph(len(evacuation_graph))
graph.graph = evacuation_graph

pos = [(482201.43764657574, 4429420.039828826), (484474.41707627784, 4420967.975494733),
       (487867.22478463524, 4425696.30418808), (487239.42871609627, 4434768.247875405)]

for x, y in pos:
    dict_ = graph.connections((x, y))

    for key in dict_.keys():
        print(f"\t{key} = {dict_[key]}")

    print("=" * 100)

graph.primMST()
