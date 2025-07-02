import random
from datetime import datetime, timedelta

from faker import Faker
from pydantic import BaseModel, ConfigDict

from backend.simulator.model.enum.animal import AnimalIcon, AnimalStatus, AnimalType
from backend.simulator.model.enum.gender import Gender
from backend.simulator.model.enum.species import Species
from backend.simulator.model.tracker import Tracker
from backend.specie_map_traits import SPECIE_TRAITS_MAP

faker = Faker()


class Animal(BaseModel):
    id: str
    tracker: Tracker
    name: str
    status: AnimalStatus = AnimalStatus.ALIVE
    icon: AnimalIcon
    species: Species
    gender: Gender
    animal_type: AnimalType
    age: float
    born_at: datetime
    deceased_at: datetime | None = None
    length_cm: float
    weight_kg: float

    model_config = ConfigDict(validate_assignment=True)

    def __init__(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        species = random.choice(list(SPECIE_TRAITS_MAP.keys()))
        traits = SPECIE_TRAITS_MAP[species]
        gender = random.choice(list(Gender))
        age = traits.random_age()

        name = {
            Gender.MALE: faker.first_name_male(),
            Gender.FEMALE: faker.first_name_female(),
            Gender.UNKNOWN: faker.first_name_nonbinary(),
        }[gender]

        super().__init__(
            id=faker.uuid4(),
            tracker=Tracker(),  # internally generated
            name=name,
            species=species,
            gender=gender,
            animal_type=traits.animal_type,
            icon=traits.icon,
            age=age,
            born_at=datetime.now() - timedelta(days=age * 365.25),
            length_cm=traits.random_length(),
            weight_kg=traits.random_weight(),
            **kwargs,
        )
