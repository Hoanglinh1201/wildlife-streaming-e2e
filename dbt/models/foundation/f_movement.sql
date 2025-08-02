{{
    config(
        materialized='incremental',
        unique_key='event_id',
        incremental_strategy='append',
    )
}}


select
    tracker_id,
    event_id,
    event_type,
    event_at,
    lat,
    lon,
    prev_lat,
    prev_lon,
    greatCircleDistance(toFloat64(prev_lat), toFloat64(prev_lon), toFloat64(lat), toFloat64(lon)) / 1000 as distance_km,
    round(distance_km / 4, 2) as speed_kmh
from {{ ref('cdc_events') }}
{% if is_incremental() %}
where event_at >= (
    select max(event_at)
    from {{ this }}
)
{% endif %}
