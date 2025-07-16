{{
    config(
        materialized='incremental',
        unique_key='animal_id',
        incremental_strategy='delete_insert',
        on_schema_change='sync_all_columns',
    )
}}


select
    animal_id,
    animal_name,
    animal_status,
    animal_icon,
    species,
    animal_type,
    gender,
    age,
    toDateTime(intDiv(born_at, 1000000)) as born_at,
    deceased_at,
    length_cm,
    weight_kg,
    tracker_id,
    current_timestamp() as dwh_created_at
from {{ ref('cdc_animals') }}
{% if is_incremental()%}
where dwh_created_at >= (
    select max(dwh_created_at)
    from {{ this }}
)
{% endif %}
qualify ROW_NUMBER() OVER (PARTITION BY animal_id ORDER BY dwh_created_at DESC) = 1
