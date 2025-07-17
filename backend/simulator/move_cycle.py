import asyncio
import logging
from uuid import uuid4

from backend.db.db_manage import get_session
from backend.db.operations import (
    insert_event,
    select_all_live_animals,
)
from backend.models.event import Event, EventType
from backend.settings import Settings
from backend.simulator.events import move

settings = Settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def move_cycle() -> None:
    """A placeholder for a background task that runs periodically."""
    while True:
        logger.info("Starting animal movement cycle...")

        with get_session() as db:
            animals = select_all_live_animals(db)

            moved_animals = [move(a) for a in animals]

            event_to_insert = [
                Event(
                    id=uuid4().hex,  # Generate a unique ID for the event
                    type=EventType.MOVE,
                    detail={
                        "animal_id": a.id,
                        "tracker_id": a.tracker.id,
                        "lat": a.tracker.lat,
                        "lon": a.tracker.lon,
                        "battery_level": a.tracker.battery_level,
                    },
                )
                for a in moved_animals
            ]

            insert_event(db, event_to_insert)

        logger.info("Animal movement cycle completed.")
        await asyncio.sleep(settings.MOVE_INTERVAL_SECONDS)
