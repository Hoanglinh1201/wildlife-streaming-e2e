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
    JSONExtractString(after, 'id') as animal_id,
    JSONExtractString(after, 'name') as animal_name,
    JSONExtractString(after, 'status') as animal_status,
    JSONExtractString(after, 'icon') as animal_icon,
    JSONExtractString(after, 'species') as species,
    JSONExtractString(after, 'animal_type') as animal_type,
    JSONExtractString(after, 'gender') as gender,
    JSONExtractFloat(after, 'age') as age,
    JSONExtractInt(after, 'born_at') as born_at,
    JSONExtractInt(after, 'deceased_at') as deceased_at,
    JSONExtractFloat(after, 'length_cm') as length_cm,
    JSONExtractFloat(after, 'weight_kg') as weight_kg,
    JSONExtractString(after, 'tracker_id') as tracker_id,

    CURRENT_TIMESTAMP() as dwh_created_at
from {{ source('landing', 'cdc_animals') }}
{% if is_incremental() %}
where dwh_created_at >= (
    select max(dwh_created_at)
    from {{ this }}
)
{% endif %}
