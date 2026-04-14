{{
    config(
        materialized='table'
    )
}}

-- NASA Silver Layer: Harmonized schema with timestamp and quality
with base as (
    select
        unit_number,
        cycle,
        op_setting_1,
        op_setting_2,
        op_setting_3,
        {{ min_max_normalize('sensor_5', 'unit_number') }} as quality,
        cycle as sensor_timestamp
    from bronze_nasa_train
)

select
    unit_number,
    cycle,
    op_setting_1,
    op_setting_2,
    op_setting_3,
    quality,
    sensor_timestamp
from base
qualify
    row_number() over (
        partition by unit_number order by cycle
    ) = 1
order by
    unit_number,
    cycle
