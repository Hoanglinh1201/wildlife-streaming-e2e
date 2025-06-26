from datetime import datetime

from pydantic import BaseModel


class Collar(BaseModel):
    id: str
    battery_level: int
    last_charged: datetime
    last_maintenance: datetime
    lat: float
    lon: float

    @property
    def is_battery_low(self) -> bool:
        return self.battery_level < 20

    @property
    def age(self) -> int:
        return (datetime.now() - self.last_charged).days
