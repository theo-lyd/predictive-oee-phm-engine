{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: OEE Final Aggregation
with ap as (
    select * from {{ ref('oee_availability_performance') }}
),

quality as (
    select
        unit_number,
        avg(quality) as quality
    from {{ ref('nasa_silver') }}
    group by unit_number
)


select
    ap.unit_number,
    ap.availability,
    ap.performance,
    q.quality,
    ap.availability * ap.performance * q.quality as oee
from ap as ap
inner join quality as q on ap.unit_number = q.unit_number
order by ap.unit_number
