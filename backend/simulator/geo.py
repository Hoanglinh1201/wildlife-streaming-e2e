import math
import random

from backend.settings import Settings

settings = Settings()

EARTH_RADIUS_KM = 6371.0


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
    lat: float, lon: float, distance_km: float, bearing_deg: float
) -> tuple[float, float]:
    """
    Calculates a new coordinate given distance and bearing from a starting lat/lon.

    Args:
        lat (float): Starting latitude in degrees
        lon (float): Starting longitude in degrees
        distance_km (float): Distance to move in kilometers
        bearing_deg (float): Bearing (direction) in degrees

    Returns:
        (lat, lon): New latitude and longitude in degrees
    """
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing_deg)
    delta = distance_km / EARTH_RADIUS_KM

    new_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(delta)
        + math.cos(lat_rad) * math.sin(delta) * math.cos(bearing_rad)
    )

    new_lon_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(delta) * math.cos(lat_rad),
        math.cos(delta) - math.sin(lat_rad) * math.sin(new_lat_rad),
    )

    return math.degrees(new_lat_rad), math.degrees(new_lon_rad)
