# app/routes/animal.py

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from simulator.server.lifespan import ANIMALS, REMOVED_ANIMALS

router = APIRouter()


@router.get("/live", response_model=list[str])
def list_live_animal_ids() -> list[str]:
    """Return all currently alive animal IDs."""
    return list(ANIMALS.keys())


@router.get("/dead", response_model=list[str])
def list_dead_animal_ids() -> list[str]:
    """Return all deceased animal IDs."""
    return list(REMOVED_ANIMALS.keys())


@router.get("/coordinates", response_model=list[dict[str, Any]])
def get_all_animal_coordinates() -> list[dict[str, Any]]:
    """Return all animals with their coordinates."""
    coordinates = [
        {
            "animal_id": k,
            "coordinate": [v.tracker.lon, v.tracker.lat],
            "timestamp": int(datetime.now().timestamp() * 1000),
        }
        for k, v in ANIMALS.items()
    ]
    return coordinates


@router.get("/tracking_metadata", response_model=list[dict[str, Any]])
def get_tracking_metadata() -> list[dict[str, Any]]:
    """Return metadata for all animals."""
    try:
        return [
            {
                "animal_id": k,
                "type": v.animal_type.value,
                "species": v.species.value,
                "icon": v.icon.value,
                "born_at": v.born_at.isoformat(),
                "age": v.age,
                "gender": v.gender,
                "length_cm": v.length_cm,
                "weight_kg": v.weight_kg,
                "tracker_id": v.tracker.id,
                "tracker_type": v.tracker.type.value,
                "tracker_battery": v.tracker.battery_level,
                "tracker_status": v.tracker.status.value,
            }
            for k, v in ANIMALS.items()
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving tracking metadata: {e!s}",
        ) from e
