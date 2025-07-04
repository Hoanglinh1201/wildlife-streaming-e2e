# simulator/backend/api/routes_animals.py


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from backend.db.db_manage import get_session
from backend.db.tables import AnimalDB, TrackerDB, TrackingLogDB
from backend.models.animal import Animal
from backend.models.tracker import Tracker, TrackingLog

router = APIRouter()
db_dep = Depends(get_session)


@router.get("/animals/{animal_id}", response_model=Animal)
def get_animal_by_id(
    animal_id: str,
    db: Session = db_dep,
) -> Animal:
    """
    Retrieve a single Animal by its ID, including its Tracker.
    """
    orm_animal = (
        db.query(AnimalDB)
        .options(joinedload(AnimalDB.tracker))
        .filter(AnimalDB.id == animal_id)
        .one_or_none()
    )
    if not orm_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    # Pydantic v2:
    return Animal.model_validate(orm_animal)


@router.get("/trackers/{tracker_id}", response_model=Tracker)
def get_tracker_by_id(
    tracker_id: str,
    db: Session = db_dep,
) -> Tracker:
    """
    Retrieve a single Tracker by its ID.
    """
    orm_tracker = db.query(TrackerDB).filter(TrackerDB.id == tracker_id).one_or_none()
    if not orm_tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return Tracker.model_validate(orm_tracker)


@router.get(
    "/animals/{animal_id}/tracking-logs",
    response_model=list[TrackingLog],
)
def get_latest_tracking_logs(
    tracker_id: str,
    limit: int = Query(10, gt=0, le=100, description="Max number of logs to return"),
    db: Session = db_dep,
) -> list[TrackingLog]:
    """
    Return the most recent `limit` tracking logs for a given animal, ordered newest-first.
    """
    logs = (
        db.query(TrackingLogDB)
        .filter(TrackingLogDB.tracker_id == tracker_id)
        .order_by(TrackingLogDB.timestamp.desc())
        .limit(limit)
        .all()
    )
    if not logs:
        # If no logs exist, you can choose to return [] or 404; here we return empty list
        return []
    return [TrackingLog.model_validate(log) for log in logs]
