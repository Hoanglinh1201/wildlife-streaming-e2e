import os
from pathlib import Path

from dagster_dbt import DbtProject

# Get the absolute path to the root of the repo
REPO_ROOT = Path(__file__).resolve().parents[1]
DBT_PROJECT_DIR = REPO_ROOT.joinpath("dbt").resolve()
DBT_TARGET = os.environ.get("DBT_TARGET", "dev")

wildlife_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    packaged_project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROJECT_DIR,
    target=DBT_TARGET,
)
wildlife_project.prepare_if_dev()
