import pickle
import heapq

# Reference: CMPSC 463 Google Colab Notebook 9
def dijkstra(graph, source):
    # Initialize the priority queue with the source node
    priority_queue = [(0, source)]  # (distance, vertex)

    # Distances dictionary to store the shortest path lengths
    distances = {vertex: float('infinity') for vertex in graph}
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
        for i in range(len(graph[current_vertex])):
            neighbor = graph[current_vertex][i][0]
            weight = graph[current_vertex][i][1]
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance,neighbor))

    return distances

def connections(graph, source):
    distances = dijkstra(graph, source)
    connections = {}
    for item in distances:
        if distances[item] != float('infinity'):
            connections[item] = distances[item]

    return connections

##################################
# Test cases with points; many inf because many points unconnected
# Graph item structure = (x1, y1) : [(x2, y2), weight]
file = "evacuation_graph.pkl"
with open(file, "rb") as f:
    evacuation_graph = pickle.load(f)

print(connections(evacuation_graph, (482201.43764657574, 4429420.039828826)))
print(connections(evacuation_graph, (484474.41707627784, 4420967.975494733)))
print(connections(evacuation_graph, (487867.22478463524, 4425696.30418808)))
print(connections(evacuation_graph, (487239.42871609627, 4434768.247875405)))
