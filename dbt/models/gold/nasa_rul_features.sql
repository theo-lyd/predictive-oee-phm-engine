{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: NASA Feature Engineering for RUL
with base as (
    select
        unit_number,
        cycle,
        {{ min_max_normalize('sensor_5', 'unit_number') }} as quality,
        cycle as sensor_timestamp,
        -- Example: Use sensor_6 as vibration
        sensor_6 as vibration,
        -- Rolling mean/variance (window=5 cycles)
        avg(sensor_6) over (
            partition by unit_number
            order by cycle
            rows between 4 preceding and current row
        ) as vibration_roll_mean_5,
        stddev_samp(sensor_6) over (
            partition by unit_number
            order by cycle
            rows between 4 preceding and current row
        ) as vibration_roll_std_5,
        -- Lag features
        lag(sensor_6, 1) over (
            partition by unit_number
            order by cycle
        ) as vibration_lag_1,
        lag(sensor_6, 2) over (
            partition by unit_number
            order by cycle
        ) as vibration_lag_2,
        -- Slope (difference from previous cycle)
        sensor_6 - lag(sensor_6, 1) over (
            partition by unit_number
            order by cycle
        ) as vibration_slope_1,
        -- RUL target
        max(cycle) over (
            partition by unit_number
        ) - cycle as rul_target
    from bronze_nasa_train
)

select *
from base
order by unit_number, cycle
