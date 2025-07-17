from dagster import Definitions
from dagster_dbt import DbtCliResource

from .alerts import alert_on_failure
from .assets import wildlife_dbt_assets
from .jobs import jobs
from .project import wildlife_project
from .schedules import schedules
from .sensors import sensors

defs = Definitions(
    assets=[wildlife_dbt_assets],
    schedules=schedules,
    sensors=[*sensors, alert_on_failure],
    jobs=jobs,
    resources={
        "dbt": DbtCliResource(project_dir=wildlife_project),
    },
)
