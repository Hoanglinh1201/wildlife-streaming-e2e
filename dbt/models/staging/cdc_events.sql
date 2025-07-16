
{{
    config(
        materialized='incremental',
        unique_key='event_id',
        incremental_strategy='delete_insert',
        on_schema_change='sync_all_columns',
    )
}}


with
parsed as (

    select
        -- Common fields
        JSONExtractString(after, 'id') AS event_id,
        JSONExtractString(after, 'type') AS event_type,
        toDateTime( intDiv(toInt64(JSONExtractString(after, 'timestamp')), 1000000)) AS event_at,
        JSONExtractString(after, 'detail') as detail_json,


        -- Detail fields
        JSONExtractString(detail_json,'animal_id') AS animal_id,
        JSONExtractString(detail_json,'tracker_id') AS tracker_id,
        JSONExtractFloat(detail_json,'lat') AS lat,
        JSONExtractFloat(detail_json,'lon') AS lon,
        JSONExtractFloat(detail_json,'battery_level') AS battery_level,
        JSONExtractString(detail_json,'remove_reason') AS remove_reason,

        -- DWH fields
        CURRENT_TIMESTAMP() AS dwh_created_at

    from {{ source('landing', 'cdc_events') }}
    {% if is_incremental()%}
    where dwh_created_at >= (
        select max(dwh_created_at)
        from {{ this }}
    )
    {% endif %}
)

select
    event_id,
    event_type,
    event_at,
    animal_id,
    tracker_id,
    lat,
    lon,
    battery_level,
    remove_reason,
    dwh_created_at
from parsed
