import asyncio
import logging
from uuid import uuid4

from backend.db.db_manage import get_session
from backend.db.operations import (
    insert_event,
    select_all_live_animals,
    upsert_animals,
    upsert_tracker,
)
from backend.models.animal import Animal
from backend.models.event import Event, EventType
from backend.models.tracker import Tracker
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

            if not animals:
                logger.info("No live animals found. Skipping move cycle.")
                await asyncio.sleep(settings.MOVE_INTERVAL_SECONDS)
                continue

            events: list[Event] = []
            animal_to_update: list[Animal] = []
            tracker_to_update: list[Tracker] = []

            for animal in animals:
                prev_lat = animal.tracker.lat
                prev_lon = animal.tracker.lon
                moved_animal = move(animal)
                events.append(
                    Event(
                        id=uuid4().hex,  # Generate a unique ID for the event
                        type=EventType.MOVE,
                        detail={
                            "animal_id": moved_animal.id,
                            "tracker_id": moved_animal.tracker.id,
                            "lat": moved_animal.tracker.lat,
                            "lon": moved_animal.tracker.lon,
                            "prev_lat": prev_lat,
                            "prev_lon": prev_lon,
                            "battery_level": moved_animal.tracker.battery_level,
                        },
                    )
                )

                animal_to_update.append(moved_animal)
                tracker_to_update.append(moved_animal.tracker)

            # Upsert animals and trackers
            upsert_animals(db, animal_to_update)
            upsert_tracker(db, tracker_to_update)
            # Insert events into the database
            insert_event(db, events)

        logger.info("Animal movement cycle completed.")
        await asyncio.sleep(settings.MOVE_INTERVAL_SECONDS)
