import logging
import math
import random

from simulator.model.animal import Animal
from simulator.model.enum.animal import AnimalStatus
from simulator.settings import Settings
from simulator.event.spawn import spawn_animal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def within_bounds(lat: float, lon: float) -> bool:
    """
    Checks if the given latitude and longitude are within the defined bounds.

    Args:
        lat (float): Latitude to check.
        lon (float): Longitude to check.

    Returns:
        bool: True if within bounds, False otherwise.
    """
    settings = Settings()
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


def move_animal(animal: Animal) -> None:
    """
    Moves the animal to a new random location within the defined bounds.

    Args:
        animal (Animal): The animal object to be moved.

    Returns:
        Animal: The updated animal object with new coordinates.
    """
    settings = Settings()

    if animal.status == AnimalStatus.DECEASED:
        logger.warning(f"Animal {animal.id} is deceased and cannot be moved.")
        return

    direction = random.randint(0, 360)  # Random direction in degrees
    delta = random.uniform(0, settings.MOVE_DELTA)  # Random distance to move

    new_lat, new_lon = calculate_new_coordinates(
        animal.tracker.lat, animal.tracker.lon, delta, direction
    )

    # Ensure the new coordinates are within bounds
    if not within_bounds(new_lat, new_lon):
        new_lat, new_lon = calculate_new_coordinates(
            animal.tracker.lat,
            animal.tracker.lon,
            delta,
            (direction + 180) % 360,  # Reverse direction if out of bounds
        )

    animal.tracker.lat = new_lat
    animal.tracker.lon = new_lon

    # After moving, battery is drained by 1% and age + 1 month
    animal.tracker.battery_level = max(0, animal.tracker.battery_level - 1)
    animal.age += 1 / 12  # Increment age by 1 month


if __name__ == "__main__":
    # Example usage
    animal = spawn_animal()
    print(f"Before moving: {animal.tracker.lat}, {animal.tracker.lon}")
    move_animal(animal)
    print(f"After moving: {animal.tracker.lat}, {animal.tracker.lon}")
