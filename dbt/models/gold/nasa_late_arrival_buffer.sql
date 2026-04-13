{{
    config(
        materialized='incremental',
        unique_key='unit_number,cycle',
        on_schema_change='sync_all_columns'
    )
}}

-- Gold Layer: Late-Arriving NASA Sensor Heartbeats Buffer
-- This model captures sensor records that arrive out of sequence (late) within a window of 5 cycles

with base as (
    select * from {{ ref('nasa_silver') }}
),

windowed as (
    select
        unit_number,
        cycle as sensor_timestamp,
        quality,
        lag(sensor_timestamp, 1) over (partition by unit_number order by sensor_timestamp) as prev_timestamp
    from base
)

select
    unit_number,
    sensor_timestamp,
    quality,
    case when prev_timestamp is not null and sensor_timestamp - prev_timestamp > 1 then 1 else 0 end as is_late_arrival
from windowed

{% if is_incremental() %}
  where sensor_timestamp > (select max(sensor_timestamp) - 5 from {{ this }})
{% endif %}
