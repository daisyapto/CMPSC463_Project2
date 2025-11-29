from shapely.geometry import Point
from Algorithms.Utilities import inside_philly, get_distance


def snap_to_nearest(graph, source):
    # Source not a Point object
    if not isinstance(source, Point):
        raise TypeError("Source must be shapely Point")

    # correct ordering
    lat, lon = source.y, source.x

    # Source not in philly
    if not inside_philly(lat, lon):
        raise ValueError("Source is outside Philadelphia")

    return min(graph.keys(), key=lambda n: get_distance((lon, lat), n))
