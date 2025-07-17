from dagster import define_asset_job
from dagster_dbt import build_dbt_asset_selection

from .assets import wildlife_dbt_assets

foundation_job = define_asset_job(
    name="foundation_update",
    selection=build_dbt_asset_selection(
        dbt_assets=[wildlife_dbt_assets], dbt_select="tag:foundation"
    ),
)

mart_job = define_asset_job(
    name="mart_update",
    selection=build_dbt_asset_selection(
        dbt_assets=[wildlife_dbt_assets], dbt_select="tag:mart"
    ),
)

jobs = [
    foundation_job,
    mart_job,
]
