{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='delete_insert',
        on_schema_change='sync_all_columns',
    )
}}


select
    id,
    JSONExtractString(after, 'id') as tracker_id,
    JSONExtractString(after, 'type') as tracker_type,
    JSONExtractString(after, 'status') as tracker_status,
    CURRENT_TIMESTAMP() as dwh_created_at

from {{ source('landing', 'cdc_trackers') }}
{% if is_incremental() %}
where dwh_created_at >= (
    select max(dwh_created_at)
    from {{ this }}
)
{% endif %}
