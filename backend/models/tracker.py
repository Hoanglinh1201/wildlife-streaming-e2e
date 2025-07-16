import random
import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TrackerType(str, Enum):
    COLLAR = "collar"
    GPS = "gps"
    RFID = "rfid"


class TrackerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Tracker(BaseModel):
    """
    Represents a tracker device used to monitor animals.
    Attributes:
        id (str): Unique identifier for the tracker.
        type (TrackerType): Type of the tracker (e.g., GPS, VHF).
        status (TrackerStatus): Current status of the tracker (e.g., active, inactive).

    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    status: TrackerStatus = TrackerStatus.ACTIVE
    type: TrackerType = Field(default_factory=lambda: random.choice(list(TrackerType)))
    lat: float = Field(default=0.0, description="Latitude of the tracker's location")
    lon: float = Field(default=0.0, description="Longitude of the tracker's location")
    battery_level: int = Field(
        default=100, description="Battery level of the tracker in percentage"
    )

    model_config = ConfigDict(from_attributes=True)
