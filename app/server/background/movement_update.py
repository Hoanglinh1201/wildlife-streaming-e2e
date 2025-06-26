import asyncio

from app.components.simulator.pack_behavior import move_pack
from app.components.utils.logging import log_pack_movement
from app.model.pack import Pack


async def update_packs_minutely(packs: list[Pack]) -> None:
    """
    Placeholder for a function that would update packs every minute.
    This could be used to simulate real-time updates or changes in the packs.
    """
    while True:
        # Simulate some update logic here
        move_logs = []
        for pack in packs:
            move_log = move_pack(pack)
            move_logs.append(move_log)

        log_pack_movement(move_logs)
        await asyncio.sleep(60)  # Wait for 1 minute before the next update
