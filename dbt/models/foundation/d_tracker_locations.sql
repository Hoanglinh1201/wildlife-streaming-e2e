
{{
    config(
        materialized='incremental',
        unique_key='tracker_id',
        incremental_strategy='delete_insert',
        on_schema_change='sync_all_columns',
    )
}}

select
    tracker_id,
    lat,
    lon,
    battery_level,
    current_timestamp() AS dwh_created_at
from {{ ref('cdc_events') }}
{% if is_incremental()%}
where dwh_created_at >= (
    select max(dwh_created_at)
    from {{ this }}
)
{% endif %}
qualify row_number() OVER (PARTITION BY tracker_id ORDER BY dwh_created_at DESC) = 1
