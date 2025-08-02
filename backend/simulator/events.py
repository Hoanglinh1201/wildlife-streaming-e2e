import logging
import random
from datetime import datetime

from backend.models.animal import SPECIE_TRAITS_MAP, Animal, AnimalStatus
from backend.models.tracker import TrackerStatus
from backend.settings import Settings
from backend.simulator.geo import (
    calculate_new_coordinates,
    random_location_within_bounds,
    within_bounds,
)

logging.basicConfig(level=logging.INFO)

settings = Settings()


def reach_max_age(animal: Animal) -> bool:
    """
    Checks if the animal is alive based on its age.

    Args:
        animal (Animal): The animal object to check.

    Returns:
        bool: True if the animal is alive, False otherwise.
    """
    max_age = SPECIE_TRAITS_MAP[animal.species].age_range[1]
    return animal.age > max_age


def remove(animal: Animal) -> Animal:
    animal.status = AnimalStatus.DECEASED
    animal.tracker.status = TrackerStatus.INACTIVE
    animal.deceased_at = datetime.now()

    return animal


def spawn() -> Animal:
    """Spawns a new animal with a tracker and initializes its attributes."""
    lat, lon = random_location_within_bounds()
    animal = Animal()
    ## Update the tracker
    animal.tracker.lat = lat
    animal.tracker.lon = lon
    logging.info(f"Spawning {animal.id} at location: ({lat}, {lon})")

    return animal


def move(animal: Animal) -> Animal:
    """Moves the animal to a new random location within bounds."""
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
    animal.tracker.battery_level = max(0, animal.tracker.battery_level - 3)
    animal.age += 1 / 6
    logging.info(f"Animal {animal.id} moved to ({new_lat}, {new_lon})")

    return animal
