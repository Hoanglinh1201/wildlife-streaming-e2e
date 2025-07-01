import asyncio
import logging

from simulator.model.animal import Animal
from simulator.model.enum.animal import AnimalStatus
from simulator.settings import Settings
from simulator.event.remove import check_and_remove_animal
from simulator.event.spawn import spawn_animal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()


async def lifecycle_animal_update(
    animals: dict[str, Animal], removed_animals: dict[str, Animal]
) -> None:
    """Spawns new animals and removes dead ones."""
    while True:
        # Remove dead animals
        for animal_id, animal in list(animals.items()):
            check_and_remove_animal(animal)
            if animal.status == AnimalStatus.DECEASED:
                del animals[animal_id]
                removed_animals[animal_id] = animal

        # Spawn new animals
        if len(animals) <= settings.ANIMAL_LIMIT:
            for _ in range(settings.SPAWN_NR):
                new_animal = spawn_animal()
                animals[new_animal.id] = new_animal

        await asyncio.sleep(settings.SPAWN_INTERVAL_SECONDS)
