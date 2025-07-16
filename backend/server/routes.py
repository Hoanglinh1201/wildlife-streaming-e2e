# simulator/backend/api/routes_animals.py


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from backend.db.db_manage import get_session
from backend.db.tables import AnimalDB, TrackerDB
from backend.models.animal import Animal
from backend.models.tracker import Tracker

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


# Healthcheck route
@router.get("/health", response_model=dict[str, str])
def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "API is healthy"}
