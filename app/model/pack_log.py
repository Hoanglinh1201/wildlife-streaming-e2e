from datetime import datetime

from pydantic import BaseModel


class PackLog(BaseModel):
    pack_name: str

    # For initialization
    type: str | None = None
    territory_size: float | None = None
    size: int | None = None
    males: int | None = None
    region: str | None = None

    # For movement
    prev_location: tuple[float, float] | None = None
    new_location: tuple[float, float] | None = None
    prev_travel_mode: str | None = None
    new_travel_mode: str | None = None
    distance_moved: float | None = None
    timestamp: datetime | None = None
