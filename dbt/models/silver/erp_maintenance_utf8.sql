{{
    config(
        materialized='table'
    )
}}

with erp_raw as (
    select * from bronze_erp_maintenance_logs
)

select
    {{ encoding_shield('Datum') }} as datum_utf8,
    {{ encoding_shield('Anlage') }} as anlage_utf8,
    {{ encoding_shield('Standort') }} as standort_utf8,
    {{ encoding_shield('Status') }} as status_utf8,
    {{ encoding_shield('"Kosten (EUR)"') }} as kosten_utf8
from erp_raw
