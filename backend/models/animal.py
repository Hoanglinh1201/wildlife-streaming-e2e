import random
from datetime import datetime, timedelta
from enum import Enum

from faker import Faker
from pydantic import BaseModel, ConfigDict

from backend.models.tracker import Tracker

faker = Faker()


DEFAULT_ICON = (
    "https://img.icons8.com/?size=100&id=hJtWtfOfjEsK&format=png&color=000000"
)


class AnimalType(str, Enum):
    MAMMAL = "mammal"
    BIRD = "bird"
    REPTILE = "reptile"
    AMPHIBIAN = "amphibian"
    FISH = "fish"
    INSECT = "insect"
    ARACHNID = "arachnid"
    OTHER = "other"


class Species(str, Enum):
    ELEPHANT = "Elephant"
    GAUR = "Gaur"
    LEOPARD = "Leopard"
    SUN_BEAR = "Sun Bear"
    DHOLE = "Dhole"
    PORCUPINE = "Porcupine"
    PANGOLIN = "Pangolin"
    MONITOR_LIZARD = "Monitor Lizard"
    HORNBILL = "Hornbill"
    PEAFOWL = "Peafowl"
    VULTURE = "Vulture"
    KINGFISHER = "Kingfisher"
    PYTHON = "Python"
    LANGUR = "Langur"
    CIVET = "Civet"
    WILD_BOAR = "Wild Boar"
    GECKO = "Gecko"
    EAGLE = "Eagle"
    OWL = "Owl"
    TORTOISE = "Tortoise"


class AnimalIcon(str, Enum):
    ELEPHANT = (
        "https://img.icons8.com/?size=100&id=aMvJw65mbqCX&format=png&color=000000"
    )
    GAUR = "https://img.icons8.com/?size=100&id=iByjK44LWaNu&format=png&color=000000"
    LEOPARD = "https://img.icons8.com/?size=100&id=lebmT3Yz7q2Q&format=png&color=000000"
    SUN_BEAR = (
        "https://img.icons8.com/?size=100&id=b9rkD77U9wsN&format=png&color=000000"
    )
    DHOLE = "https://img.icons8.com/?size=100&id=67tg2TQBcKAM&format=png&color=000000"
    PORCUPINE = (
        "https://img.icons8.com/?size=100&id=d2ssoe1zIlGg&format=png&color=000000"
    )
    PANGOLIN = (
        "https://img.icons8.com/?size=100&id=d2ssoe1zIlGg&format=png&color=000000"
    )
    MONITOR_LIZARD = (
        "https://img.icons8.com/?size=100&id=oa2bHbtiJaYF&format=png&color=000000"
    )
    HORNBILL = (
        "https://img.icons8.com/?size=100&id=qTxbyl0tqoKL&format=png&color=000000"
    )
    PEAFOWL = "https://img.icons8.com/?size=100&id=QrhSO3jG3Fgp&format=png&color=000000"
    VULTURE = "https://img.icons8.com/?size=100&id=5ycpDAJhYTbT&format=png&color=000000"
    KINGFISHER = (
        "https://img.icons8.com/?size=100&id=qTxbyl0tqoKL&format=png&color=000000"
    )
    PYTHON = "https://img.icons8.com/?size=100&id=6Tpb4xpmgZk7&format=png&color=000000"
    LANGUR = "https://img.icons8.com/?size=100&id=qLTrKDR4K61i&format=png&color=000000"
    CIVET = "https://img.icons8.com/?size=100&id=l7kbLnDvLZwI&format=png&color=000000"
    WILD_BOAR = (
        "https://img.icons8.com/?size=100&id=HaaDZW8y3oCJ&format=png&color=000000"
    )
    GECKO = "https://img.icons8.com/?size=100&id=oa2bHbtiJaYF&format=png&color=000000"
    EAGLE = "https://img.icons8.com/?size=100&id=FumKjKiTArzQ&format=png&color=000000"
    OWL = "https://img.icons8.com/?size=100&id=lrSRHnxYFj2O&format=png&color=000000"
    TORTOISE = (
        "https://img.icons8.com/?size=100&id=G3uBZC9dmTix&format=png&color=000000"
    )


class AnimalStatus(str, Enum):
    """
    Enum for different statuses of an animal.
    """

    ALIVE = "alive"
    DECEASED = "deceased"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


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


SPECIE_TRAITS_MAP: dict[Species, SpecieTrait] = {
    Species.ELEPHANT: SpecieTrait(
        name="Elephant",
        age_range=(5, 60),
        length_range=(250, 700),
        weight_range=(2000, 6000),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.ELEPHANT,
    ),
    Species.GAUR: SpecieTrait(
        name="Gaur",
        age_range=(3, 20),
        length_range=(250, 350),
        weight_range=(600, 1000),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.GAUR,
    ),
    Species.LEOPARD: SpecieTrait(
        name="Leopard",
        age_range=(2, 17),
        length_range=(90, 150),
        weight_range=(30, 90),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.LEOPARD,
    ),
    Species.SUN_BEAR: SpecieTrait(
        name="Sun Bear",
        age_range=(2, 25),
        length_range=(100, 150),
        weight_range=(30, 80),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.SUN_BEAR,
    ),
    Species.DHOLE: SpecieTrait(
        name="Dhole",
        age_range=(1, 10),
        length_range=(80, 120),
        weight_range=(10, 25),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.DHOLE,
    ),
    Species.PORCUPINE: SpecieTrait(
        name="Porcupine",
        age_range=(1, 15),
        length_range=(40, 90),
        weight_range=(5, 15),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.PORCUPINE,
    ),
    Species.PANGOLIN: SpecieTrait(
        name="Pangolin",
        age_range=(1, 10),
        length_range=(40, 100),
        weight_range=(4, 12),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.PANGOLIN,
    ),
    Species.MONITOR_LIZARD: SpecieTrait(
        name="Monitor Lizard",
        age_range=(1, 20),
        length_range=(70, 200),
        weight_range=(5, 30),
        animal_type=AnimalType.REPTILE,
        icon=AnimalIcon.MONITOR_LIZARD,
    ),
    Species.HORNBILL: SpecieTrait(
        name="Hornbill",
        age_range=(2, 40),
        length_range=(70, 120),
        weight_range=(2, 4),
        animal_type=AnimalType.BIRD,
        icon=AnimalIcon.HORNBILL,
    ),
    Species.PEAFOWL: SpecieTrait(
        name="Peafowl",
        age_range=(1, 15),
        length_range=(90, 200),
        weight_range=(3, 6),
        animal_type=AnimalType.BIRD,
        icon=AnimalIcon.PEAFOWL,
    ),
    Species.VULTURE: SpecieTrait(
        name="Vulture",
        age_range=(2, 30),
        length_range=(80, 130),
        weight_range=(5, 12),
        animal_type=AnimalType.BIRD,
        icon=AnimalIcon.VULTURE,
    ),
    Species.KINGFISHER: SpecieTrait(
        name="Kingfisher",
        age_range=(1, 10),
        length_range=(15, 25),
        weight_range=(0.05, 0.1),
        animal_type=AnimalType.BIRD,
        icon=AnimalIcon.KINGFISHER,
    ),
    Species.PYTHON: SpecieTrait(
        name="Python",
        age_range=(1, 25),
        length_range=(200, 600),
        weight_range=(20, 90),
        animal_type=AnimalType.REPTILE,
        icon=AnimalIcon.PYTHON,
    ),
    Species.LANGUR: SpecieTrait(
        name="Langur",
        age_range=(1, 20),
        length_range=(40, 75),
        weight_range=(5, 15),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.LANGUR,
    ),
    Species.CIVET: SpecieTrait(
        name="Civet",
        age_range=(1, 15),
        length_range=(50, 90),
        weight_range=(3, 7),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.CIVET,
    ),
    Species.WILD_BOAR: SpecieTrait(
        name="Wild Boar",
        age_range=(1, 12),
        length_range=(100, 180),
        weight_range=(50, 150),
        animal_type=AnimalType.MAMMAL,
        icon=AnimalIcon.WILD_BOAR,
    ),
    Species.GECKO: SpecieTrait(
        name="Gecko",
        age_range=(1, 8),
        length_range=(10, 30),
        weight_range=(0.02, 0.2),
        animal_type=AnimalType.REPTILE,
        icon=AnimalIcon.GECKO,
    ),
    Species.EAGLE: SpecieTrait(
        name="Eagle",
        age_range=(3, 25),
        length_range=(60, 100),
        weight_range=(3, 7),
        animal_type=AnimalType.BIRD,
        icon=AnimalIcon.EAGLE,
    ),
    Species.OWL: SpecieTrait(
        name="Owl",
        age_range=(2, 20),
        length_range=(30, 60),
        weight_range=(1, 4),
        animal_type=AnimalType.BIRD,
        icon=AnimalIcon.OWL,
    ),
    Species.TORTOISE: SpecieTrait(
        name="Tortoise",
        age_range=(5, 100),
        length_range=(20, 100),
        weight_range=(10, 200),
        animal_type=AnimalType.REPTILE,
        icon=AnimalIcon.TORTOISE,
    ),
}


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

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

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
            tracker=Tracker(),
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
