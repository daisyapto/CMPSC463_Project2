import heapq, math
from Algorithms.Utilities import get_distance


# Reference: https://www.geeksforgeeks.org/dsa/prims-minimum-spanning-tree-mst-greedy-algo-5/
def prim_mst(evac_coords):
    n = len(evac_coords)
    if n <= 1:
        return []

    # Start with first evac
    visited = [False] * n
    smallest_edge = [math.inf] * n
    parent = [-1] * n
    smallest_edge[0] = 0
    mst_edges = []

    for _ in range(n):
        # Pick the unvisited node with smallest edge
        current_node = min((w, i) for i, w in enumerate(smallest_edge) if not visited[i])[1]
        visited[current_node] = True

        # Add the current node to the MST
        if parent[current_node] != -1:
            mst_edges.append((evac_coords[parent[current_node]], evac_coords[current_node]))

        # Update best edges to neighbors
        for neighbor in range(n):
            if not visited[neighbor]:
                dist = get_distance(evac_coords[current_node], evac_coords[neighbor])
                # Smaller distance found, update parent
                if dist < smallest_edge[neighbor]:
                    smallest_edge[neighbor] = dist
                    parent[neighbor] = current_node
    return mst_edges
