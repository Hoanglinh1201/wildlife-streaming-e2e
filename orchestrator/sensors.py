# orchestrator/sensors.py

from dagster import (
    DagsterRunStatus,
    RunRequest,
    RunStatusSensorContext,
    run_status_sensor,
)

from .jobs import foundation_job, mart_job
from .schedules import cdc_schedule


@run_status_sensor(
    name="trigger_foundation_after_cdc",
    monitored_jobs=[cdc_schedule.job],
    run_status=DagsterRunStatus.SUCCESS,
    request_job=foundation_job,
)
def trigger_foundation_after_cdc(context: RunStatusSensorContext) -> RunRequest:
    context.log.info("CDC job succeeded, triggering foundation job.")
    return RunRequest(job_name=foundation_job.name)


@run_status_sensor(
    name="trigger_mart_after_foundation",
    monitored_jobs=[foundation_job],
    run_status=DagsterRunStatus.SUCCESS,
    request_job=mart_job,
)
def trigger_mart_after_foundation(context: RunStatusSensorContext) -> RunRequest:
    context.log.info("Foundation job succeeded, triggering mart job.")
    return RunRequest(job_name=mart_job.name)


sensors = [trigger_foundation_after_cdc, trigger_mart_after_foundation]
