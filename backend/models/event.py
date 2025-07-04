from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """
    Enum for different types of events in the wildlife tracking system.
    """

    SPAWN = "spawn"
    MOVE = "move"
    REMOVE = "remove"


class Event(BaseModel):
    """
    Represents an event in the wildlife tracking system.
    Attributes:
        id (str): Unique identifier for the event.
        type (str): Type of the event (e.g., sighting, tracking).
        timestamp (int): Timestamp of the event in milliseconds since epoch.
        description (str): Description of the event.
    """

    id: str = Field(default_factory=lambda: uuid4().hex)
    type: EventType
    detail: dict[str, Any] | None = (
        None  # Use a dictionary to store event-specific details
    )
    timestamp: datetime = Field(default_factory=datetime.now)
