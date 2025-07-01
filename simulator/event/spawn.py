import logging
import random

from simulator.model.animal import Animal
from simulator.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def spawn_animal() -> Animal:
    """
    Spawns a new animal with a tracker and initializes its attributes."""

    lat, lon = random_location_within_bounds()
    animal = Animal()

    ## Update the tracker
    animal.tracker.lat = lat
    animal.tracker.lon = lon

    return animal


if __name__ == "__main__":
    # Example usage
    for _ in range(settings.SPAWN_NR):
        new_animal = spawn_animal()
        spawn_log = new_animal.model_dump()
        logger.info(f"Spawned animal: {spawn_log}")
