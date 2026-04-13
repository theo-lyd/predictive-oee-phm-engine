# dbt Commands Log

Append all dbt-related commands here with timestamp, objective, command, and outcome.

---
2026-04-13: Batch 2.1 (Silver Layer)
- Objective: Encoding normalization and German string handling for ERP data
- Command: python3 scripts/ingest_erp_to_duckdb.py
- Command: dbt run --project-dir dbt --profiles-dir dbt
- Outcome: Both erp_maintenance_utf8 and erp_maintenance_normalized tables created and validated in DuckDB. All requirements for Batch 2.1 complete.

---
2026-04-13: Batch 2.2 (Silver Layer)
- Objective: Numeric harmonization and surrogate key generation for ERP data
- Command: dbt run --select silver.erp_maintenance_numeric --project-dir dbt --profiles-dir dbt
- Command: dbt run --select silver.erp_maintenance_surrogate --project-dir dbt --profiles-dir dbt
- Outcome: Both erp_maintenance_numeric and erp_maintenance_surrogate tables created and validated in DuckDB. All requirements for Batch 2.2 complete.
