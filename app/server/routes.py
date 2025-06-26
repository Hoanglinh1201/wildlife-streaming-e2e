from fastapi import APIRouter, HTTPException

from app.model.collar import Collar
from app.model.pack import Pack
from app.model.wolf import Wolf

# In-memory storage
from app.server.lifespan import COLLAR_INDEX, PACK_INDEX, PACKS, WOLF_INDEX

router = APIRouter()


# --- 1. Get list of packs ---
@router.get("/packs")
def list_packs() -> list[str]:
    """Retrieve a list of all pack IDs."""
    return list(PACK_INDEX.keys())  # ← return a list, not a dict


# --- 2. Get pack by ID---
@router.get("/packs/{pack_id}", response_model=Pack)
def get_pack(pack_id: str) -> Pack:
    """Retrieve a pack by its unique ID."""
    pack = next((p for p in PACKS if p.id == pack_id), None)
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")
    return pack


# --- 4. Get wolf by ID ---
@router.get("/wolves/{wolf_id}", response_model=Wolf)
def get_wolf(wolf_id: str) -> Wolf:
    """Retrieve a wolf by its unique ID."""
    wolf = WOLF_INDEX.get(wolf_id)
    if not wolf:
        raise HTTPException(status_code=404, detail="Wolf not found")
    return wolf


# --- 3. Get collar by ID ---
@router.get("/collars/{collar_id}", response_model=Collar)
def get_collar(collar_id: str) -> Collar:
    """Retrieve a collar by its unique ID."""
    collar = COLLAR_INDEX.get(collar_id)
    if not collar:
        raise HTTPException(status_code=404, detail="Collar not found")
    return collar
