{% snapshot erp_equipment_status_snapshot %}

    {{
        config(
            target_schema='main',
            unique_key='universal_asset_id',
            strategy='check',
            check_cols=['status']
        )
    }}

    select
        universal_asset_id,
        datum as status_date,
        status
    from {{ ref('erp_maintenance_surrogate') }}

{% endsnapshot %}
