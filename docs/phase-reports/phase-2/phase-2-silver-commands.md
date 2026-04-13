# Phase 2: Silver Layer Command Log

## Batch 2.1: Encoding & String Normalization and Character Mapping

### Objective
Implement robust encoding normalization and German string handling for ERP data in the Silver layer using dbt.

### Key Steps
- Ingested ERP logs (ISO-8859-1) into DuckDB using Python and pandas (ensures UTF-8 in warehouse).
- Developed dbt model `erp_maintenance_utf8` to provide a clean, UTF-8 version of the ERP data.
- Developed dbt model `erp_maintenance_normalized` to apply SQL regex replacements for German Umlaute, abbreviations, and character mappings.
- Refactored normalization logic to use direct chained replacements in the model for maintainability and SQL compatibility.
- Validated that both models run successfully and produce correct outputs (200 rows each).

### Commands Executed

- `python3 scripts/ingest_erp_to_duckdb.py`  
  *Ingest ERP logs into DuckDB (Bronze layer)*
- `dbt run --project-dir dbt --profiles-dir dbt`  
  *Build Silver layer models for encoding normalization and German string handling*

### Outcome
- Both `erp_maintenance_utf8` and `erp_maintenance_normalized` tables created and validated in DuckDB.
- All requirements for Batch 2.1 are complete and operational.
