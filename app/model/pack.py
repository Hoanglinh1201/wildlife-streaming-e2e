import logging
import math

from pydantic import BaseModel

from app.model.enum import TravelMode, WolfType
from app.model.wolf import Wolf
from app.settings import Settings

logging.basicConfig(level=logging.INFO)

settings = Settings()


class Pack(BaseModel):
    name: str
    type: WolfType
    leader: Wolf
    members: list[Wolf]
    territory_size: float  # in square kilometers
    travel_mode: TravelMode = TravelMode.IDLE  # Default travel mode
    start_lat: float = 0.0  # Initial latitude, will be set later
    start_lon: float = 0.0  # Initial longitude, will be set later
    lat: float = 0.0  # Initial latitude, will be set later
    lon: float = 0.0  # Initial longitude, will be set later
    movement_speed: float = 0.0  # Calculated based on travel mode

    @property
    def id(self) -> str:
        """
        Generate a unique ID for the pack based on its name.
        """
        return f"wolf_pack_{self.name.lower().replace(' ', '_')}"

    @property
    def territory_radius(self) -> float:
        """
        Calculate the radius of the pack's territory based on its size.
        The formula for the area of a circle is A = πr², so r = √(A/π).
        """
        return math.sqrt(self.territory_size / math.pi)
