{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: OEE Availability & Performance Models
with silver as (
    select * from {{ ref('nasa_silver') }}
),

-- Calculate planned and operating time per unit (example logic, adjust as needed)
operating_time as (
    select
        unit_number,
        count(*) as operating_time
    from silver
    group by unit_number
),

planned_time as (
    select
        unit_number,
        max(sensor_timestamp) - min(sensor_timestamp) + 1 as planned_time
    from silver
    group by unit_number
),

throughput as (
    select
        unit_number,
        count(*) as actual_throughput
    from silver
    group by unit_number
),

target_throughput as (
    select
        unit_number,
        max(sensor_timestamp) as target_throughput
    from silver
    group by unit_number
)

select
    o.unit_number,
    o.operating_time,
    p.planned_time,
    t.actual_throughput,
    tt.target_throughput,
    cast(o.operating_time as double)
        / nullif(p.planned_time, 0) as availability,
    cast(t.actual_throughput as double)
        / nullif(tt.target_throughput, 0) as performance
from operating_time AS o
inner join planned_time AS p on o.unit_number = p.unit_number
inner join throughput AS t on o.unit_number = t.unit_number
inner join target_throughput AS tt on o.unit_number = tt.unit_number
