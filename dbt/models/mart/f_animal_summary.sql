with

descriptive as (

    select
        animals.animal_id,
        animals.animal_name,
        animals.animal_status,
        animals.animal_icon,
        animals.species,
        animals.animal_type,
        animals.gender,
        animals.age,
        animals.born_at,
        animals.deceased_at,
        animals.length_cm,
        animals.weight_kg,
        trackers.tracker_id as tracker_id,
        trackers.tracker_type,
        trackers.tracker_status,
        trackers.lat,
        trackers.lon,
        trackers.battery_level,
        trackers.dwh_created_at as tracker_location_at
    from {{ ref('d_animals') }} as animals
    left join {{ ref('d_trackers') }} as trackers
        on animals.tracker_id = trackers.tracker_id
),

movement_metrics as (

    select
        tracker_id,
        count(*) as total_movements,
        -- Movement distance metrics
        avg(distance_km) as avg_movement_distance,
        max(distance_km) as max_movement_distance,
        min(distance_km) as min_movement_distance,
        sum(distance_km) as total_movement_distance,
        -- Speed metrics
        avg(speed_kmh) as avg_speed,
        max(speed_kmh) as max_speed,
        min(speed_kmh) as min_speed
    from {{ ref('f_movement') }}
    where event_type = 'move'
    group by tracker_id

)

select
    descriptive.*,
    movement_metrics.total_movements,
    movement_metrics.avg_movement_distance,
    movement_metrics.max_movement_distance,
    movement_metrics.min_movement_distance,
    movement_metrics.total_movement_distance,
    movement_metrics.avg_speed,
    movement_metrics.max_speed,
    movement_metrics.min_speed
from descriptive
left join movement_metrics
    on descriptive.tracker_id = movement_metrics.tracker_id
