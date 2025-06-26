import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.components.simulator.initialize import initialize_packs
from app.model.pack import Pack
from app.server.background.movement_update import update_packs_minutely

# In-memory storage
PACKS: list[Pack] = []
PACK_INDEX = {}
WOLF_INDEX = {}
COLLAR_INDEX = {}

background_tasks = []


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize the lifespan of the FastAPI application"""
    global PACKS, PACK_INDEX, WOLF_INDEX, COLLAR_INDEX
    PACKS = initialize_packs()
    for pack in PACKS:
        PACK_INDEX[pack.id] = pack
        for wolf in pack.members:
            WOLF_INDEX[wolf.id] = wolf
            COLLAR_INDEX[wolf.collar.id] = wolf.collar

    task = asyncio.create_task(update_packs_minutely(PACKS))
    background_tasks.append(task)
    yield
