{{
    config(
        materialized='table'
    )
}}

-- NASA Silver Layer: Harmonized schema with timestamp and quality
with base as (
    select
        cast("0" as integer) as unit_number,
        cast("1" as integer) as cycle,
        cast("2" as double) as op_setting_1,
        cast("3" as double) as op_setting_2,
        cast("4" as double) as op_setting_3,
        {{ min_max_normalize('"5"', 'cast("0" as integer)') }} as quality,
        cast("1" as integer) as sensor_timestamp
    from bronze_nasa_train
)

select unit_number, cycle, op_setting_1, op_setting_2, op_setting_3, quality, sensor_timestamp
from base
qualify row_number() over (partition by unit_number order by cycle) = 1
order by unit_number, cycle
