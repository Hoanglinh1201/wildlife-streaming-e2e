import logging
import math
import random

from app.components.simulator.locations import WOLF_LOCATIONS
from app.components.utils.geo_helper import haversine_km, offset_location
from app.components.utils.randomize import randomize_travel_mode
from app.model.enum import WolfType
from app.model.pack import Pack
from app.model.pack_log import PackLog
from app.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


def km_per_minute(speed_kmh: float) -> float:
    return speed_kmh / 60.0


def territory_radius_km(territory_size_km2: float) -> float:
    return math.sqrt(territory_size_km2 / math.pi)


def get_start_location(pack_type: WolfType) -> tuple[float, float, str]:
    """
    Select a random location based on the pack type.
    Returns a tuple of (latitude, longitude).
    """
    matching_locations = [loc for loc in WOLF_LOCATIONS if loc.type == pack_type]
    if not matching_locations:
        raise ValueError(f"No locations found for pack type: {pack_type}")

    chosen = random.choice(matching_locations)

    lat = random.uniform(chosen.lat_range.min, chosen.lat_range.max)
    lon = random.uniform(chosen.lon_range.min, chosen.lon_range.max)

    return lat, lon, chosen.region


def initialize_pack(pack: Pack) -> PackLog:
    """
    Assign starting location and movement speed to the pack.
    """

    lat, lon, region = get_start_location(pack.type)

    pack.start_lat = lat
    pack.start_lon = lon
    pack.lat = lat
    pack.lon = lon

    set_travel_mode(pack)
    update_pack_collars(pack)

    # Stats
    nr_of_wolves = len(pack.members)
    nr_male_wolves = sum(1 for wolf in pack.members if wolf.gender == "male")

    return PackLog(
        pack_name=pack.name,
        type=pack.type,
        territory_size=pack.territory_size,
        new_location=(lat, lon),
        new_travel_mode=pack.travel_mode,
        size=nr_of_wolves,
        males=nr_male_wolves,
        region=region,
    )


def set_travel_mode(pack: Pack) -> None:
    """
    Set the pack's movement speed (in km/min) based on its travel mode.
    """
    speed_map = {
        "idle": 0.0,
        "trot": random.uniform(8.0, 10.0),
        "lope": random.uniform(12.0, 15.0),
        "sprint": random.uniform(20.0, 25.0),
    }
    pack.travel_mode = randomize_travel_mode()
    pack.movement_speed = km_per_minute(speed_map.get(pack.travel_mode, 8.0))


def move_pack(pack: Pack) -> PackLog:
    """
    Move the pack randomly within its territory. Reverse direction if outside bounds.
    """
    distance_km = pack.movement_speed
    direction = random.uniform(0, 360)

    meters_per_deg_lat = 111_320
    meters_per_deg_lon = 111_320 * math.cos(math.radians(pack.lat))

    delta_lat = (
        distance_km * 1000 * math.cos(math.radians(direction))
    ) / meters_per_deg_lat
    delta_lon = (
        distance_km * 1000 * math.sin(math.radians(direction))
    ) / meters_per_deg_lon

    next_lat = pack.lat + delta_lat
    next_lon = pack.lon + delta_lon

    radius_km = territory_radius_km(pack.territory_size)
    dist_from_center = haversine_km(next_lat, next_lon, pack.start_lat, pack.start_lon)

    if dist_from_center > radius_km:
        logger.warning(
            f"⚠️ Pack {pack.name} moving outside its territory. Reversing direction."
        )
        direction = (direction + 180) % 360
        delta_lat = (
            distance_km * 1000 * math.cos(math.radians(direction))
        ) / meters_per_deg_lat
        delta_lon = (
            distance_km * 1000 * math.sin(math.radians(direction))
        ) / meters_per_deg_lon
        next_lat = pack.lat + delta_lat
        next_lon = pack.lon + delta_lon

    # Apply new position
    prev_lat = pack.lat
    prev_lon = pack.lon
    prev_travel_mode = pack.travel_mode
    pack.lat = next_lat
    pack.lon = next_lon

    update_pack_collars(pack)
    pack.travel_mode = randomize_travel_mode()
    set_travel_mode(pack)

    return PackLog(
        pack_name=pack.name,
        prev_location=(prev_lat, prev_lon),
        new_location=(next_lat, next_lon),
        prev_travel_mode=prev_travel_mode,
        new_travel_mode=pack.travel_mode,
        distance_moved=haversine_km(prev_lat, prev_lon, next_lat, next_lon),
    )


def update_pack_collars(pack: Pack) -> None:
    """
    Update each wolf's collar position based on the current pack location.
    """
    for wolf in pack.members:
        if wolf.is_leader:
            wolf.collar.lat = pack.lat
            wolf.collar.lon = pack.lon
        else:
            offset_lat, offset_lon = offset_location(
                pack.lat, pack.lon, max_offset_m=500
            )
            wolf.collar.lat = offset_lat
            wolf.collar.lon = offset_lon
