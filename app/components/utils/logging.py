from datetime import datetime

from rich.console import Console
from rich.table import Table

from app.model.pack_log import PackLog


def log_pack_creation_summary(logs: list[PackLog]) -> None:
    console = Console()
    table = Table(title="Wolf Pack Initialization Summary")

    table.add_column("Pack Name", style="bold cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Territory Size", style="blue")
    table.add_column("Location", justify="right")
    table.add_column("Travel Mode", style="yellow")
    table.add_column("# Wolves", justify="center")
    table.add_column("# Males", justify="center")
    table.add_column("Region", style="green")

    for log in logs:
        table.add_row(
            log.pack_name,
            log.type or "-",
            f"{log.territory_size:.2f} km²" if log.territory_size else "-",
            f"({log.new_location[0]:.4f},{log.new_location[1]:.4f})"
            if log.new_location
            else "-",
            log.new_travel_mode or "-",
            str(log.size) if log.size is not None else "-",
            str(log.males) if log.males is not None else "-",
            log.region or "-",
        )

    console.print(table)


def log_pack_movement(logs: list[PackLog]) -> None:
    console = Console()
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table = Table(title=f"Wolf Pack Movement Log - {timestamp_str}")

    table.add_column("Pack Name", style="bold cyan")
    table.add_column("Prev Location", justify="right")
    table.add_column("New Location", justify="right")
    table.add_column("Prev Travel Mode", style="yellow")
    table.add_column("New Travel Mode", style="yellow")
    table.add_column("Distance Moved (km)", style="blue")

    for log in logs:
        table.add_row(
            log.pack_name,
            f"({log.prev_location[0]:.4f},{log.prev_location[1]:.4f})"
            if log.prev_location
            else "-",
            f"({log.new_location[0]:.4f},{log.new_location[1]:.4f})"
            if log.new_location
            else "-",
            log.prev_travel_mode or "-",
            log.new_travel_mode or "-",
            f"{log.distance_moved:.2f}" if log.distance_moved is not None else "-",
        )

    console.print(table)
