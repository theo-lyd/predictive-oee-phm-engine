{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: NASA Sensor Data with Integrity Contracts
with base as (
    select
        cast("0" as integer) as unit_number,
        cast("1" as integer) as cycle,
        {{ min_max_normalize('"5"', 'cast("0" as integer)') }} as quality,
        cast("1" as integer) as sensor_timestamp
    from bronze_nasa_train
)

select unit_number, cycle, quality, sensor_timestamp
from base
qualify row_number() over (partition by unit_number order by cycle) = 1
order by unit_number, cycle
