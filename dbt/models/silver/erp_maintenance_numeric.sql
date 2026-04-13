{{
    config(
        materialized='table'
    )
}}

with normalized as (
    select * from {{ ref('erp_maintenance_normalized') }}
)

select
    datum,
    anlage,
    standort,
    status,
    -- German numeric parser: convert e.g. '1.234,56' to 1234.56
    cast(replace(replace(kosten, '.', ''), ',', '.') as double) as kosten_eur
from normalized
