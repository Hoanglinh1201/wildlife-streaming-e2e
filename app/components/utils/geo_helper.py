import math
import random


def offset_location(
    lat: float, lon: float, max_offset_m: int = 500
) -> tuple[float, float]:
    """
    Generate a location offset from the given lat/lon by up to max_offset_m meters.
    """
    # 1 degree latitude ≈ 111,320 meters
    meters_per_deg_lat = 111_320
    meters_per_deg_lon = 111_320 * math.cos(math.radians(lat))

    # Random distance and bearing
    distance_m = random.uniform(100, max_offset_m)
    bearing = random.uniform(0, 360)

    # Convert distance to degrees
    delta_lat = (distance_m * math.cos(math.radians(bearing))) / meters_per_deg_lat
    delta_lon = (distance_m * math.sin(math.radians(bearing))) / meters_per_deg_lon

    return lat + delta_lat, lon + delta_lon


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the Haversine distance between two points on the Earth specified in decimal degrees.
    Returns the distance in kilometers."""
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c
