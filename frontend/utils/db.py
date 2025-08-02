import os

import pandas as pd
from clickhouse_driver import Client


def get_clickhouse_client() -> Client:
    """
    Create a ClickHouse client instance.
    """
    return Client(
        host=os.getenv("CLICKHOUSE_HOST", "localhost"),
        port=os.getenv("CLICKHOUSE_PORT", "9000"),
        user=os.getenv("CLICKHOUSE_USER", "consumer"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "consumer"),
        database=os.getenv("CLICKHOUSE_DATABASE", "mart"),
    )


def compile_sql(sql_template: str, params: dict[str, str] | None = None) -> str:
    """
    Compile the SQL template with the provided parameters.

    :param sql_template: The SQL template string with placeholders.
    :param params: A dictionary of parameters to replace in the template.
    :return: A compiled SQL string.
    """
    injectable_params = params or {}
    return sql_template.format(**injectable_params)


def query_clickhouse(sql: str, params: dict[str, str] | None = None) -> pd.DataFrame:
    """
    Execute a SQL query on ClickHouse and return the result as a DataFrame.

    :param sql: The SQL query to execute.
    :param params: Optional parameters for the SQL query.
    :return: A pandas DataFrame containing the query results.
    """
    client = get_clickhouse_client()
    compiled_sql = compile_sql(sql, params)
    result = client.execute(compiled_sql, with_column_types=True)
    columns = [col[0] for col in result[1]]

    # Convert the result to a DataFrame
    df = pd.DataFrame(result[0], columns=columns)
    return df
