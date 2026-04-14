{{
    config(
        materialized='table'
    )
}}

with numeric as (
    select * from {{ ref('erp_maintenance_numeric') }}
)

select
    *,
    {{ dbt_utils.generate_surrogate_key([
        'datum',
        'anlage',
        'standort'
    ]) }} as universal_asset_id
from numeric
