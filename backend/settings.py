from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Wild Life Collar Tracker"
    NATIONAL_PARK_NAME: str = "YOK DON NATIONAL PARK"
    NP_REGION: str = "Central Highlands, Vietnam"
    NP_LAT_RANGE: tuple[float, float] = (
        12.5,
        14.0,
    )  # Latitude range of the national park
    NP_LON_RANGE: tuple[float, float] = (
        107.0,
        108.5,
    )  # Longitude range of the national park
    NP_AREA: float = 1150.0  # Area in square kilometers

    # LIMITS
    ANIMAL_LIMIT: int = 50  # Maximum number of animals in the park

    # Lifecycle
    LIFECYCLE_UPDATE_INTERVAL: int = 60  # Spawn animals every seconds
    SPAWN_NR: int = 5  # Number of animals to spawn each time

    # Move
    MOVE_DELTA: float = 0.2  # Distance in km to move each animal per cycle
    MOVE_INTERVAL_SECONDS: int = 15  # Update packs every seconds
