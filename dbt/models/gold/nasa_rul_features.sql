{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: NASA Feature Engineering for RUL
with base as (
    select
        cast("0" as integer) as unit_number,
        cast("1" as integer) as cycle,
        {{ min_max_normalize('"5"', 'cast("0" as integer)') }} as quality,
        cast("1" as integer) as sensor_timestamp,
        -- Example: Use sensor 6 (column 5) as vibration
        cast("5" as double) as vibration,
        -- Rolling mean/variance (window=5 cycles)
        avg(cast("5" as double)) over (partition by cast("0" as integer) order by cast("1" as integer) rows between 4 preceding and current row) as vibration_roll_mean_5,
        stddev_samp(cast("5" as double)) over (partition by cast("0" as integer) order by cast("1" as integer) rows between 4 preceding and current row) as vibration_roll_std_5,
        -- Lag features
        lag(cast("5" as double), 1) over (partition by cast("0" as integer) order by cast("1" as integer)) as vibration_lag_1,
        lag(cast("5" as double), 2) over (partition by cast("0" as integer) order by cast("1" as integer)) as vibration_lag_2,
        -- Slope (difference from previous cycle)
        cast("5" as double) - lag(cast("5" as double), 1) over (partition by cast("0" as integer) order by cast("1" as integer)) as vibration_slope_1,
        -- RUL target
        max(cast("1" as integer)) over (partition by cast("0" as integer)) - cast("1" as integer) as rul_target
    from bronze_nasa_train
)

select *
from base
order by unit_number, cycle
