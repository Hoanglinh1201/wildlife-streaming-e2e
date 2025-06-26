import logging

from faker import Faker

from app.components.simulator.pack_behavior import initialize_pack
from app.components.utils.logging import log_pack_creation_summary
from app.components.utils.randomize import (
    randomize_born_date,
    randomize_gender,
    randomize_health_status,
    randomize_pack_name,
    randomize_pack_size,
    randomize_pack_type,
    randomize_territory_size,
)
from app.model.collar import Collar
from app.model.enum import Gender, HealthStatus, TravelMode
from app.model.pack import Pack
from app.model.pack_log import PackLog
from app.model.wolf import Wolf
from app.settings import Settings

settings = Settings()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_collar() -> Collar:
    """
    Create a collar with a unique ID and default attributes.
    """
    return Collar(
        id=Faker().uuid4(),
        battery_level=100,
        last_charged=Faker().date_time_this_year(),
        last_maintenance=Faker().date_time_this_year(),
        lat=0.0,  # Will be updated later with pack initialization
        lon=0.0,  # Will be updated later with pack initialization
    )


def create_leader_wolf() -> Wolf:
    """
    Create a leader wolf with specific attributes.
    The leader wolf will have a unique ID and be assigned a collar.
    """
    return Wolf(
        name=Faker().first_name_male(),
        is_leader=True,
        born_date=randomize_born_date(modifer=5),
        collar=create_collar(),
        health_status=HealthStatus.HEALTHY,
        gender=Gender.MALE,
        last_seen=Faker().date_time_this_year().isoformat(),
        notes=Faker().sentence(nb_words=20),
    )


def create_wolf() -> Wolf:
    """Create a wolf with a unique ID and attributes."""
    gender = randomize_gender()
    name = (
        Faker().first_name_female() if gender == "female" else Faker().first_name_male()
    )
    return Wolf(
        name=name,
        is_leader=False,
        born_date=randomize_born_date(),
        collar=create_collar(),
        health_status=randomize_health_status(),
        gender=gender,
        last_seen=Faker().date_time_this_year().isoformat(),
        notes=Faker().sentence(nb_words=20),
    )


def create_pack() -> tuple[Pack, PackLog]:
    """Create a pack of wolves with a leader and members."""
    pack_size = randomize_pack_size()
    leader = create_leader_wolf()
    members = [leader]  # Start with the leader in the pack
    for _ in range(pack_size - 1):
        members.append(create_wolf())

    pack = Pack(
        name=randomize_pack_name(),
        type=randomize_pack_type(),
        leader=leader,
        members=members,
        territory_size=randomize_territory_size(),
        travel_mode=TravelMode.IDLE,  # Once the pack is initialized, the travel mode will be updated based on behavior
    )

    pack_creation_log = initialize_pack(pack)
    return pack, pack_creation_log


def initialize_packs() -> list[Pack]:
    """
    Initialize the Wild Life Collar Tracker application.
    This function sets up the necessary configurations and prepares the application for use.
    """

    logger.info("Initializing Wild Life Collar Tracker...")

    # Create packs and wolves
    packs = []
    logs = []
    for _ in range(settings.NR_PACKS):
        pack, pack_creation_log = create_pack()
        packs.append(pack)
        logs.append(pack_creation_log)

    logger.info(f"Initialized {len(packs)} packs with wolves.")
    log_pack_creation_summary(logs)

    # Rich table output for pack creation logs

    return packs
