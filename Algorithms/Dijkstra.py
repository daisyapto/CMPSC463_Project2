import heapq
from Algorithms.Snap_Centers import snap_to_nearest
from shapely.geometry import Point

def dijkstra(graph, source):
    # source is a Point(lon, lat)
    if source not in graph:
        source = snap_to_nearest(graph, source)

    heap = [(0, source)]
    distances = {v: float("inf") for v in graph}
    previous = {v: None for v in graph}
    distances[source] = 0


    while heap:
        dist, current_node = heapq.heappop(heap)
        if dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_distance = dist + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(heap, (new_distance, neighbor))

    # keep only reachable nodes
    return distances, previous

def get_path(graph, previous, goal):
    if goal not in previous:
        goal = snap_to_nearest(graph, Point(goal[0], goal[1]))
        # Unreachable goal even after snapping
        if goal not in previous:
            return []

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path