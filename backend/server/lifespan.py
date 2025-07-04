import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.db.db_manage import init_db
from backend.settings import Settings
from backend.simulator.cycles import move_cycle, spawn_cycle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    spawn_task = asyncio.create_task(spawn_cycle())
    move_task = asyncio.create_task(move_cycle())

    try:
        yield  # App runs here
    finally:
        # Cleanup happens here
        move_task.cancel()
        spawn_task.cancel()
        await asyncio.gather(spawn_task, return_exceptions=True)
