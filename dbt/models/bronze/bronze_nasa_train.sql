{{
    config(
        materialized='view'
    )
}}

{{
    config(
        materialized='view'
    )
}}

-- Select from the physical DuckDB table
select * from bronze_nasa_train_physical
