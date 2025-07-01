import random
import uuid

from pydantic import BaseModel, Field

from simulator.model.enum.tracker import TrackerStatus, TrackerType


class Tracker(BaseModel):
    """
    Represents a tracker device used to monitor animals.
    Attributes:
        id (str): Unique identifier for the tracker.
        type (TrackerType): Type of the tracker (e.g., GPS, VHF).
        battery_level (int): Current battery level percentage (0-100).
        last_charged (datetime): Timestamp of the last charging event.
        last_maintenance (datetime): Timestamp of the last maintenance check.
        lat (float): Current latitude of the tracker.
        lon (float): Current longitude of the tracker.
        is_battery_low (bool): Indicates if the battery level is below a threshold.

    """

    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    status: TrackerStatus = TrackerStatus.ACTIVE
    type: TrackerType = Field(default_factory=lambda: random.choice(list(TrackerType)))
    battery_level: int = Field(default_factory=lambda: random.randint(20, 100))
    lat: float = 0.0  # Always initialized to 0.0 and gets updated later with spawning
    lon: float = 0.0  # Always initialized to 0.0 and gets updated later with spawning
