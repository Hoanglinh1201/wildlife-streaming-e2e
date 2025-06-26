from pydantic import BaseModel

from app.model.enum import WolfType


class Range(BaseModel):
    min: float
    max: float


class Location(BaseModel):
    name: str
    lat_range: Range
    lon_range: Range
    region: str
    type: WolfType
