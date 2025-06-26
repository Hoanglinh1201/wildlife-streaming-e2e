from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Wild Life Collar Tracker"

    # Pack Setting
    NR_PACKS: int = 10
    MIN_WOLF_PER_PACK: int = 5
    MAX_WOLF_PER_PACK: int = 15
    MIN_AGE_WOLF: int = 1
    MAX_AGE_WOLF: int = 15

    MIN_TERRITORY_SIZE_KM2: int = 200
    MAX_TERRITORY_SIZE_KM2: int = 300

    MALE_RATIO: int = 75

    HEALTHY_PROB: int = 90
    SICK_PROB: int = 5
    INJURED_PROB: int = 5
