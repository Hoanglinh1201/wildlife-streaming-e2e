import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload

from backend.db.tables import AnimalDB, EventDB, TrackerDB
from backend.models.animal import Animal, AnimalStatus
from backend.models.event import Event
from backend.models.tracker import Tracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def select_all_live_animals(db: Session) -> list[Animal]:
    """
    Retrieve all live animals from the database.
    """

    orm_animals = (
        db.query(AnimalDB)
        .options(joinedload(AnimalDB.tracker))
        .filter(AnimalDB.status == AnimalStatus.ALIVE)
        .all()
    )
    # Convert each ORM instance into a Pydantic model
    return [Animal.model_validate(a) for a in orm_animals]


def upsert_animals(db: Session, animals: list[Animal]) -> None:
    rows = []
    for a in animals:
        # Convert Animal to AnimalDB, excluding tracker
        data = a.model_dump()
        data["tracker_id"] = a.tracker.id
        data.pop("tracker", None)  # Remove tracker from the data
        rows.append(data)

    ins = insert(AnimalDB).values(rows)
    stmt = ins.on_conflict_do_update(
        constraint="animals_pkey",
        set_={
            "tracker_id": ins.excluded.tracker_id,
            "name": ins.excluded.name,
            "status": ins.excluded.status,
            "icon": ins.excluded.icon,
            "species": ins.excluded.species,
            "gender": ins.excluded.gender,
            "age": ins.excluded.age,
            "born_at": ins.excluded.born_at,
            "deceased_at": ins.excluded.deceased_at,
            "length_cm": ins.excluded.length_cm,
            "weight_kg": ins.excluded.weight_kg,
        },
    )
    db.execute(stmt)
    logger.info(f"Upserted {len(rows)} animals into the database.")


def upsert_tracker(db: Session, trackers: list[Tracker]) -> None:
    rows = [t.model_dump(exclude={"lat", "lon", "battery_level"}) for t in trackers]
    ins = insert(TrackerDB).values(rows)
    stmt = ins.on_conflict_do_update(
        index_elements=[TrackerDB.id],
        set_={
            "type": ins.excluded.type,
            "status": ins.excluded.status,
        },
    )
    db.execute(stmt)
    logger.info(f"Upserted {len(rows)} trackers into the database.")


def insert_event(db: Session, events: list[Event]) -> None:
    rows = [e.model_dump() for e in events]
    stmt = insert(EventDB).values(rows)
    db.execute(stmt)
    logger.info(f"Inserted {len(rows)} events into the database.")
