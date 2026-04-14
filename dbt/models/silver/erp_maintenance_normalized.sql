{{
    config(
        materialized='table'
    )
}}

with erp_utf8 as (
    select * from {{ ref('erp_maintenance_utf8') }}
)

select
    regexp_replace(
        regexp_replace(
            regexp_replace(datum_utf8, 'ü', 'ue'),
            'Ü', 'Ue'
        ),
        'ö', 'oe'
    ) as datum,
    regexp_replace(
        regexp_replace(
            regexp_replace(anlage_utf8, 'ä', 'ae'),
            'Ä', 'Ae'
        ),
        'ß', 'ss'
    ) as anlage,
    regexp_replace(
        regexp_replace(standort_utf8, 'ö', 'oe'),
        'Ö', 'Oe'
    ) as standort,
    regexp_replace(
        regexp_replace(status_utf8, 'Wartung', 'Service'),
        'Störung', 'Stoerung'
    ) as status,
    regexp_replace(
        regexp_replace(kosten_utf8, 'EUR', 'Euro'),
        ',', '.'
    ) as kosten
from erp_utf8
