import math
import random

from backend.settings import Settings

settings = Settings()


def random_location_within_bounds() -> tuple[float, float]:
    """
    Generates a random latitude and longitude within the specified bounds.

    Args:
        lat_range (tuple[float, float]): Tuple containing min and max latitude.
        lon_range (tuple[float, float]): Tuple containing min and max longitude.

    Returns:
        tuple[float, float]: Random latitude and longitude within the specified bounds.
    """
    lat = random.uniform(settings.NP_LAT_RANGE[0], settings.NP_LAT_RANGE[1])
    lon = random.uniform(settings.NP_LON_RANGE[0], settings.NP_LON_RANGE[1])
    return lat, lon


def within_bounds(lat: float, lon: float) -> bool:
    """
    Checks if the given latitude and longitude are within the defined bounds.

    Args:
        lat (float): Latitude to check.
        lon (float): Longitude to check.

    Returns:
        bool: True if within bounds, False otherwise.
    """
    return (
        settings.NP_LAT_RANGE[0] <= lat <= settings.NP_LAT_RANGE[1]
        and settings.NP_LON_RANGE[0] <= lon <= settings.NP_LON_RANGE[1]
    )


def calculate_new_coordinates(
    lat: float, lon: float, delta: float, direction: float
) -> tuple[float, float]:
    """
    Calculates new coordinates based on the current latitude, longitude, distance to move (delta), and direction.

    Args:
        lat (float): Current latitude.
        lon (float): Current longitude.
        delta (float): Distance to move in degrees.
        direction (float): Direction in degrees.

    Returns:
        tuple[float, float]: New latitude and longitude after moving.
    """
    radians = math.radians(direction)
    new_lat = lat + delta * math.cos(radians)
    new_lon = lon + delta * math.sin(radians)
    return new_lat, new_lon
