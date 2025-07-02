import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.server.background.lifecycle_animal_update import lifecycle_animal_update
from backend.server.background.move_update import move_animal_task
from backend.settings import Settings
from backend.simulator.model.animal import Animal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

# In-memory storage
ANIMALS: dict[str, Animal] = {}
REMOVED_ANIMALS: dict[str, Animal] = {}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global ANIMALS, REMOVED_ANIMALS

    move_task = asyncio.create_task(move_animal_task(ANIMALS))
    lifecycle_task = asyncio.create_task(
        lifecycle_animal_update(ANIMALS, REMOVED_ANIMALS)
    )

    try:
        yield  # App runs here
    finally:
        # Cleanup happens here
        move_task.cancel()
        lifecycle_task.cancel()
        await asyncio.gather(move_task, lifecycle_task, return_exceptions=True)
