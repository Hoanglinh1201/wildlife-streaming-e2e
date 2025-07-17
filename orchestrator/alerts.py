# orchestrator/failure_alerts.py

from datetime import UTC, datetime

from dagster import DagsterRunStatus, RunStatusSensorContext, run_status_sensor

from .jobs import foundation_job, mart_job
from .schedules import cdc_schedule


@run_status_sensor(
    name="alert_on_failure",
    monitored_jobs=[cdc_schedule.job, foundation_job, mart_job],
    run_status=DagsterRunStatus.FAILURE,
)
def alert_on_failure(context: RunStatusSensorContext) -> None:
    failed_job = context.dagster_run.job_name
    ts = datetime.now(tz=UTC).isoformat()
    context.log.error(f"🚨 Job `{failed_job}` failed at {ts}.")

    return None
