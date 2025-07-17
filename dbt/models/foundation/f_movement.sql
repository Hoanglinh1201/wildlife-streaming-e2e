{{
    config(
        materialized='incremental',
        unique_key='event_id',
        incremental_strategy='append',
    )
}}

with

new_loc as (

    select
        event_id,
        event_type,
        event_at,
        tracker_id,
        lat,
        lon,
        'new' as loc_flag,
        current_timestamp() as dwh_created_at
    from {{ ref('cdc_events') }}
    {% if is_incremental() %}
    where dwh_created_at >= (
        select max(dwh_created_at)
        from {{ this }}
    )
    {% endif %}
),

prev_loc as (

    {% if is_incremental() %}
    select
        event_id,
        event_type,
        event_at,
        tracker_id,
        lat,
        lon,
        'prev' as loc_flag,
        current_timestamp() as dwh_created_at
    from {{ this }}
    qualify row_number() over (partition by tracker_id order by event_at desc) = 1
    {% else %}
    select
        null as event_id,
        null as event_type,
        null as event_at,
        null as tracker_id,
        null as lat,
        null as lon,
        'prev' as loc_flag,
        current_timestamp() as dwh_created_at
    {% endif %}

),

movement_base as (

    select * from new_loc
    union all
    select * from prev_loc

),

final as (

    select
        tracker_id,
        event_id,
        event_type,
        event_at,
        lat,
        lon,
        case
            when event_type = 'spawn' then null
            else lag(event_at) over (partition by tracker_id order by event_at)
        end as prev_event_at,

        case
            when event_type = 'spawn' then lat
            else lag(lat) over (partition by tracker_id order by event_at)
        end as prev_lat,

        case
            when event_type = 'spawn' then lon
            else lag(lon) over (partition by tracker_id order by event_at) as raw_prev_lon
        end as prev_lon,

        case
            when event_type = 'spawn' then 0
            else greatCircleDistance(toFloat64(prev_lat), toFloat64(prev_lon), toFloat64(lat), toFloat64(lon)) / 1000
        end as distance_km,

        case
            when event_type = 'spawn' then 0
            else dateDiff('second', prev_event_at, event_at) / 3600.0
        end as hours_diff,

        case
            when event_type = 'spawn' then 0
            else round(distance_km / hours_diff, 2)
        end as speed_kmh

    from movement_base
    where loc_flag = 'new'

)

select
    tracker_id,
    event_id,
    event_type,
    event_at,
    lat,
    lon,
    prev_lat,
    prev_lon,
    distance_km,
    hours_diff,
    speed_kmh
from final
order by tracker_id, event_at
