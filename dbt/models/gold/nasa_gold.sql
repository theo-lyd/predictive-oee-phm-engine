{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: NASA Sensor Data with Integrity Contracts
with base as (
    select
        unit_number,
        cycle,
        {{ min_max_normalize('sensor_5', 'unit_number') }} as quality,
        cycle as sensor_timestamp
    from bronze_nasa_train
)

select
    unit_number,
    cycle,
    quality,
    sensor_timestamp
from base
qualify row_number() over (partition by unit_number order by cycle) = 1
order by unit_number, cycle
