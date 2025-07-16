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
    tracker_type,
    tracker_status,
    current_timestamp() as dwh_created_at
from {{ ref('cdc_trackers') }}
{% if is_incremental()%}
where dwh_created_at >= (
    select max(dwh_created_at)
    from {{ this }}
)
{% endif %}
qualify ROW_NUMBER() OVER (PARTITION BY tracker_id ORDER BY dwh_created_at DESC) = 1
