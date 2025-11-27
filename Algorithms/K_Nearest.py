from Algorithms.Dijkstra import dijkstra, get_path
from Algorithms.Snap_Centers import snap_to_nearest


def k_nearest_evacuation_centers(graph, source, snapped_centers, K, tree):
    # Snap source to nearest node
    if source not in graph:
        source = snap_to_nearest(graph, source)
        # Snapped source still not in graph
        if source not in graph:
            return []

    dists, indexes = tree.query([(source[0], source[1])], k=min(K + 10, len(snapped_centers)))
    candidate_indices = indexes[0]

    print("Running Dijkstra...")
    distances, previous = dijkstra(graph, source)

    results = []

    for i in candidate_indices:
        snapped_node = snapped_centers[i]

        if snapped_node is None:
            continue

        # not reachable
        if snapped_node == float("inf"):
            continue

        path = get_path(graph, previous, snapped_node)
        if not path:
            continue

        results.append((snapped_node, distances[snapped_node], path))

    results.sort(key=lambda x: x[1])  # sort by distance
    return results[:K]
