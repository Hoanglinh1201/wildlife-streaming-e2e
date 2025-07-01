from pydantic import BaseModel

from simulator.model.enum.animal import AnimalIcon, AnimalType


class SpecieTrait(BaseModel):
    name: str
    age_range: tuple[float, float]
    length_range: tuple[float, float]
    weight_range: tuple[float, float]
    animal_type: AnimalType
    icon: AnimalIcon

    def random_age(self) -> float:
        from random import uniform

        return round(uniform(*self.age_range), 1)

    def random_length(self) -> float:
        from random import uniform

        return round(uniform(*self.length_range), 1)

    def random_weight(self) -> float:
        from random import uniform

        return round(uniform(*self.weight_range), 2)
