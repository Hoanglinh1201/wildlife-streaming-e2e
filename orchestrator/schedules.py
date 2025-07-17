# orchestrator/schedules.py

from dagster_dbt import build_schedule_from_dbt_selection

from orchestrator.assets import wildlife_dbt_assets

cdc_schedule = build_schedule_from_dbt_selection(
    job_name="cdc_integration",
    cron_schedule="0/5 * * * *",  # every hour at minute 3
    dbt_select="tag:cdc",
    dbt_assets=[wildlife_dbt_assets],
)

schedules = [cdc_schedule]
