import math


def get_distance(point_1, point_2):
    # Confirm valid points
    if len(point_1) != 2 or len(point_2) != 2:
        raise ValueError("Points must be (x, y) tuples")

    # Calculate distance using Pythagorean theorem
    x = point_1[0] - point_2[0]
    y = point_1[1] - point_2[1]
    return math.hypot(x, y)


def inside_philly(lat, lon):
    return (39.86 <= lat <= 40.14) and (-75.30 <= lon <= -74.96)
