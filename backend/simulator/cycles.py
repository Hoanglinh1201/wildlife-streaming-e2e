import asyncio
import logging

from backend.db.db_manage import get_session
from backend.db.operations import (
    insert_event,
    insert_tracking_log,
    select_all_live_animals,
    upsert_animals,
    upsert_tracker,
)
from backend.models.animal import Animal
from backend.models.event import Event, EventType
from backend.models.tracker import Tracker, TrackingLog
from backend.settings import Settings
from backend.simulator.events import move, reach_max_age, remove, spawn

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
                    type=EventType.MOVE,
                    detail={
                        "animal_id": a.id,
                        "lat": a.tracker.lat,
                        "lon": a.tracker.lon,
                    },
                )
                for a in moved_animals
            ]

            tracking_log_to_insert = [
                TrackingLog(
                    tracker_id=a.tracker.id,
                    lat=a.tracker.lat,
                    lon=a.tracker.lon,
                    battery_level=a.tracker.battery_level,
                )
                for a in moved_animals
            ]

            if event_to_insert:
                insert_event(db, event_to_insert)
                logger.info(
                    f"Inserted {len(event_to_insert)} move events into the database."
                )

            if tracking_log_to_insert:
                insert_tracking_log(db, tracking_log_to_insert)
                logger.info(
                    f"Inserted {len(tracking_log_to_insert)} tracking logs into the database."
                )

        logger.info("Animal movement cycle completed.")
        await asyncio.sleep(settings.MOVE_INTERVAL_SECONDS)


async def spawn_cycle() -> None:
    """
    From the lifecycle of the animal, this function checks for dead animals and spawns new ones
    if the number of animals is below the limit.
    - Get all animals from the database.
    - Check if any animal is dead and remove it from the pack.
    - If the number of animals is below the limit, spawn new animals.
    """
    while True:
        logger.info("Starting animal lifecycle update...")
        # Initlialize lists to hold animals, trackers, events, and tracking logs to be updated or inserted
        animal_to_update: list[Animal] = []
        tracker_to_update: list[Tracker] = []
        event_to_insert: list[Event] = []
        tracking_log_to_insert: list[TrackingLog] = []

        with get_session() as db:
            animals = select_all_live_animals(db)

            # Remove due to age
            age_check = [a if reach_max_age(a) else None for a in animals]
            to_remove: list[Animal] = [remove(a) for a in age_check if a is not None]

            # Spawn new animals if below the limit
            live_animals_amount = len(animals) - len(to_remove)
            to_spawn: list[Animal] = []
            if live_animals_amount < settings.ANIMAL_LIMIT:
                spawn_count = settings.ANIMAL_LIMIT - live_animals_amount
                for _ in range(spawn_count):
                    new_animal = spawn()
                    to_spawn.append(new_animal)

            # Records to db
            animal_to_update.extend(to_spawn + to_remove)
            tracker_to_update = [a.tracker for a in animal_to_update]

            event_to_insert.extend(
                Event(
                    type=EventType.REMOVE,
                    detail={"animal_id": a.id, "reason": "reached max age"},
                )
                for a in to_remove
            )

            event_to_insert.extend(
                Event(
                    type=EventType.SPAWN,
                    detail={"animal_id": a.id, "species": a.species},
                )
                for a in to_spawn
            )

            tracking_log_to_insert.extend(
                TrackingLog(
                    tracker_id=a.tracker.id,
                    lat=a.tracker.lat,
                    lon=a.tracker.lon,
                    battery_level=a.tracker.battery_level,
                )
                for a in to_spawn
            )

            # Perform database operations
            if animal_to_update:
                upsert_animals(db, animal_to_update)
                upsert_tracker(db, tracker_to_update)
                logger.info(
                    f"Updated {len(animal_to_update)} animals and {len(tracker_to_update)} trackers."
                )

            if event_to_insert:
                insert_event(db, event_to_insert)
                logger.info(f"Inserted {len(event_to_insert)} events.")

            if tracking_log_to_insert:
                insert_tracking_log(db, tracking_log_to_insert)
                logger.info(f"Inserted {len(tracking_log_to_insert)} tracking logs.")

        logger.info("Animal lifecycle update completed.")
        await asyncio.sleep(settings.LIFECYCLE_UPDATE_INTERVAL)
