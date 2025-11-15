import heapq


def get_nearest_vertex(graph, point):
    px, py = point
    best = None
    best_dist = float('inf')

    for (vx, vy) in graph.keys():
        d = (vx - px) ** 2 + (vy - py) ** 2
        if d < best_dist:
            best_dist = d
            best = (vx, vy)

    return best, best_dist ** 0.5


def dijkstra(graph, source):
    if source not in graph:
        source = get_nearest_vertex(graph, source)

    # Initialize the priority queue with the source node
    priority_queue = [(0, source)]  # (distance, vertex)

    # Distances dictionary to store the shortest path lengths
    distances = {vertex: float('inf') for vertex in graph}
    distances[source] = 0

    previous = {vertex: None for vertex in graph}

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
        for neighbor, weight in graph[current_vertex]:
            new_dist = current_distance + weight  # Current total weight to node
            if new_dist < distances[neighbor]:  # shorter path to neighbor found
                distances[neighbor] = new_dist  # update distance
                previous[neighbor] = current_vertex  # update previous node
                heapq.heappush(priority_queue, (new_dist, neighbor))  # update priority queue

    return distances, previous


# Build path arrays from user position to each evac center
def path_to_evac(previous, start, end):
    path = []  # Store the nodes from start to end
    current = end

    # Continue until end is found
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous[current]

    path.reverse()
    return path


def find_nearest_evacuation_center(graph, start, evac_gjs, distances, previous):
    routes = []

    # Filter coordinates from evacuation centers
    evac_centers = [(geom.x, geom.y) for geom in evac_gjs.geometry]

    for center in evac_centers:
        goal, distance = get_nearest_vertex(graph, center)  # snap evac center to road vertex

        if goal is None:
            continue

        # Get routes of reachable nodes from start to goal
        if distances.get(goal, float('inf')) != float('inf'):
            path = path_to_evac(previous, start, goal)
            routes.append([path, distances[goal], center])

    routes.sort(key=lambda x: x[1])
    return routes
