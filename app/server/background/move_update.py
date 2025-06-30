import asyncio

from app.model.animal import Animal
from app.settings import Settings
from app.simulator.move import move_animal

settings = Settings()


async def move_animal_task(animals: dict[str, Animal]) -> None:
    """A placeholder for a background task that runs periodically."""
    while True:
        for animal in animals.values():
            move_animal(animal)
        await asyncio.sleep(settings.MOVE_INTERVAL_SECONDS)
