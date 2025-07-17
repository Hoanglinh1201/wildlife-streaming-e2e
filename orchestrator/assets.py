from collections.abc import Iterator

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliInvocation, DbtCliResource, dbt_assets

from .project import wildlife_project


@dbt_assets(manifest=wildlife_project.manifest_path)
def wildlife_dbt_assets(
    context: AssetExecutionContext, dbt: DbtCliResource
) -> Iterator[DbtCliInvocation]:
    yield from dbt.cli(["build"], context=context).stream()
