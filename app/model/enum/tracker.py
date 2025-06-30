from enum import Enum


class TrackerType(str, Enum):
    COLLAR = "collar"
    GPS = "gps"
    RFID = "rfid"


class TrackerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
