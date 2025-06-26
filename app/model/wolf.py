import hashlib
from datetime import date

from pydantic import BaseModel

from app.model.collar import Collar
from app.model.enum import Gender, HealthStatus


class Wolf(BaseModel):
    name: str
    is_leader: bool
    born_date: date
    collar: Collar
    health_status: HealthStatus
    gender: Gender
    last_seen: str
    notes: str

    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.born_date.year
            - ((today.month, today.day) < (self.born_date.month, self.born_date.day))
        )

    @property
    def id(self) -> str:
        ## Generate a hash unique ID based on the wolf's name and pack ID
        unique_string = f"{self.name}-{self.born_date.isoformat()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()
