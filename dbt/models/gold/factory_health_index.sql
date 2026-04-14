{{
    config(
        materialized='table'
    )
}}

-- Gold Layer: Factory Health Index (FHI)
-- Combines OEE and normalized RUL into a single metric per asset

with oee as (
    select
        unit_number,
        oee
    from {{ ref('oee_final') }}
),

-- Get latest predicted RUL per unit from the best model
rul as (
    select
        unit_number,
        avg(rul_pred) as avg_rul_pred
    from {{ ref('nasa_rul_regressor') }}
    group by unit_number
),

-- Normalize RUL (higher RUL = healthier)
rul_norm as (
    select
        unit_number,
        (
            avg_rul_pred - min(avg_rul_pred) over ()
        ) / nullif(
            max(avg_rul_pred) over () - min(avg_rul_pred) over (), 0
        ) as rul_normalized
    from rul
)

select
    oee.unit_number,
    oee.oee,
    rul_norm.rul_normalized,
    0.5 * oee.oee + 0.5 * rul_norm.rul_normalized as factory_health_index
from oee
inner join rul_norm on oee.unit_number = rul_norm.unit_number
order by oee.unit_number
