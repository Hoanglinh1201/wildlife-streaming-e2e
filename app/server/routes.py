# app/routes/animal.py

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from app.model.animal import Animal
from app.model.tracker import Tracker
from app.server.lifespan import ANIMALS, REMOVED_ANIMALS

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.get("/live", response_model=list[str])
def list_live_animal_ids() -> list[str]:
    """Return all currently alive animal IDs."""
    return list(ANIMALS.keys())


@router.get("/dead", response_model=list[str])
def list_dead_animal_ids() -> list[str]:
    """Return all deceased animal IDs."""
    return list(REMOVED_ANIMALS.keys())


@router.get("/{animal_id}", response_model=Animal)
def get_animal_by_id(animal_id: str) -> Animal:
    """Return full animal data by ID."""
    animal = ANIMALS.get(animal_id) or REMOVED_ANIMALS.get(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.get("/{animal_id}/tracker", response_model=Tracker)
def get_tracker_by_animal_id(animal_id: str) -> Tracker:
    """Return the tracker assigned to the animal."""
    animal = ANIMALS.get(animal_id) or REMOVED_ANIMALS.get(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal.tracker


@router.get("/coordinates", response_model=list[dict[str, Any]])
def get_all_animal_coordinates() -> list[dict[str, Any]]:
    """Return all animals with their coordinates."""
    coordinates = [
        {
            "id": k,
            "coordinate": [v.tracker.lon, v.tracker.lat],
            "timestamp": int(datetime.now().timestamp() * 1000),
        }
        for k, v in ANIMALS.items()
    ]
    return coordinates
