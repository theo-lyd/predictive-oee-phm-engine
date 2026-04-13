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
        -- Min-max normalize sensor 6 (column "5") per unit to get quality between 0 and 1
        (cast("5" as double) - min(cast("5" as double)) over (partition by cast("0" as integer))) /
        nullif(max(cast("5" as double)) over (partition by cast("0" as integer)) - min(cast("5" as double)) over (partition by cast("0" as integer)), 0)
        as quality,
        -- Use cycle as the strictly increasing timestamp per unit
        cast("1" as integer) as sensor_timestamp,
        *
    from bronze_nasa_train
)

select *
from base
qualify row_number() over (partition by unit_number order by cycle) = 1
order by unit_number, cycle
