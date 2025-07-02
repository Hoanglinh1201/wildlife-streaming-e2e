import logging
from datetime import datetime

from backend.simulator.model.animal import Animal
from backend.simulator.model.enum.animal import AnimalStatus
from backend.simulator.model.enum.tracker import TrackerStatus
from backend.specie_map_traits import SPECIE_TRAITS_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_and_remove_animal(animal: Animal) -> None:
    """
    Checks if the animal is dead and removes it from the pack if so.

    Args:
        animal (Animal): The animal object to check.

    Returns:
        bool: True if the animal was removed, False otherwise.
    """

    traits = SPECIE_TRAITS_MAP[animal.species]
    max_age = traits.age_range[1]

    if (
        animal.status == AnimalStatus.DECEASED
        or animal.tracker.status == TrackerStatus.INACTIVE
        or animal.age >= max_age
    ):
        reasons = []
        if animal.status == AnimalStatus.DECEASED:
            reasons.append(f"  • Status: {animal.status}")
        if animal.tracker.status == TrackerStatus.INACTIVE:
            reasons.append(f"  • Tracker: {animal.tracker.status}")
        if animal.age >= max_age:
            reasons.append(f"  • Age: {animal.age:.1f} (max: {max_age})")

        reason_log = "\n".join(reasons)
        logger.info(f"Removed Animal {animal.id} due to:\n{reason_log}")

        animal.status = AnimalStatus.DECEASED
        animal.tracker.status = TrackerStatus.INACTIVE
        animal.tracker.battery_level = 0
        animal.deceased_at = datetime.now()


if __name__ == "__main__":
    # Example usage
    animal = Animal()
    max_age = SPECIE_TRAITS_MAP[animal.species].age_range[1]
    animal.age = max_age
    check_and_remove_animal(animal)
