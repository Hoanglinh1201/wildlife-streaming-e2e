from enum import Enum


class TravelMode(str, Enum):
    IDLE = "idle"
    TROT = "trot"
    LOPE = "lope"
    SPRINT = "sprint"
