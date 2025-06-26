import random
from datetime import date

from faker import Faker

from app.model.enum import Gender, HealthStatus, PackName, TravelMode, WolfType
from app.settings import Settings

settings = Settings()


def randomize_health_status() -> HealthStatus:
    """
    Randomly select a health status for a wolf.
    """
    weights = [settings.HEALTHY_PROB, settings.SICK_PROB, settings.INJURED_PROB]
    return random.choices(
        [HealthStatus.HEALTHY, HealthStatus.SICK, HealthStatus.INJURED],
        weights=weights,
        k=1,
    )[0]


def randomize_gender() -> Gender:
    """
    Randomly select a gender for a wolf.
    """
    weights = [settings.MALE_RATIO, 100 - settings.MALE_RATIO]
    return random.choices([Gender.MALE, Gender.FEMALE], weights=weights, k=1)[0]


def randomize_travel_mode() -> TravelMode:
    return random.choices(
        [TravelMode.IDLE, TravelMode.TROT, TravelMode.LOPE, TravelMode.SPRINT],
        weights=[5, 80, 10, 5],
    )[0]


def randomize_pack_name() -> PackName:
    """
    Randomly select a pack name from the predefined list.
    """
    return random.choice(list(PackName))


def randomize_pack_type() -> WolfType:
    """
    Randomly select a pack type from the settings.
    """
    return random.choice(list(WolfType))


def randomize_territory_size() -> float:
    """
    Randomly select a territory size for a pack.
    """
    return random.uniform(
        settings.MIN_TERRITORY_SIZE_KM2, settings.MAX_TERRITORY_SIZE_KM2
    )


def randomize_born_date(modifer: int = 0) -> date:
    """
    Randomly select a born date for a wolf within the specified age range.
    """
    return Faker().date_of_birth(
        minimum_age=settings.MIN_AGE_WOLF + modifer,
        maximum_age=settings.MAX_AGE_WOLF + modifer,
    )


def randomize_pack_size() -> int:
    """
    Randomly select a pack size within the specified range.
    """
    return random.randint(settings.MIN_WOLF_PER_PACK, settings.MAX_WOLF_PER_PACK)
