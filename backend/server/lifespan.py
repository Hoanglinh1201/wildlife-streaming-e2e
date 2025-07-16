import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.db.db_manage import init_db
from backend.settings import Settings
from backend.simulator.move_cycle import move_cycle
from backend.simulator.spawn_cycle import spawn_cycle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()


async def delay_move_cycle(delay_by_seconds: int = 5) -> None:
    try:
        await asyncio.sleep(delay_by_seconds)
        await move_cycle()
    except asyncio.CancelledError:
        logger.info("Move cycle task was cancelled.")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()

    spawn_task = asyncio.create_task(spawn_cycle())
    move_task = asyncio.create_task(delay_move_cycle())

    try:
        yield  # App runs here
    finally:
        # Cleanup happens here
        move_task.cancel()
        spawn_task.cancel()
        await asyncio.gather(spawn_task, return_exceptions=True)
