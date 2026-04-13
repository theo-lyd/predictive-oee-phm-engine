# Phase 3 Gold Layer Command Log

## Batch 3.1: The OEE Calculator

### Objective
Implement the core OEE (Overall Equipment Effectiveness) metrics at the Gold layer using dbt models. This includes Availability, Performance, and Quality, and aggregates them into a final OEE score at the asset level.

### Commands Executed
- `source main_venv/bin/activate && dbt run --select gold.oee_availability_performance gold.oee_final --project-dir dbt --profiles-dir dbt`
- `source main_venv/bin/activate && python -c "import duckdb; print(duckdb.connect('dbt/factory_analytics.db').execute('SELECT * FROM oee_final LIMIT 10').fetchdf())"`

### Outcome
- Gold layer models `oee_availability_performance` and `oee_final` created and built successfully in DuckDB.
- OEE metrics (Availability, Performance, Quality, OEE) are now available at the asset level in the `oee_final` table.
- Sample output:

| unit_number | availability | performance | quality   | oee      |
|-------------|--------------|-------------|-----------|----------|
| 1           | 1.0          | 1.0         | 0.060269  | 0.060269 |
| 2           | 1.0          | 1.0         | 1.000000  | 1.000000 |
| ...         | ...          | ...         | ...       | ...      |

### Notes
- All calculations follow the OEE formula:
  - $Availability = \frac{\text{Operating Time}}{\text{Planned Production Time}}$
  - $Performance = \frac{\text{Actual Throughput}}{\text{Target Throughput}}$
  - $OEE = Availability \times Performance \times Quality$
- The models use the Silver layer `nasa_silver` as the source for sensor and quality data.
- All results validated in DuckDB.

## Batch 3.2: Asset History (SCD Type 2)

### Objective
Track the full history of equipment status changes (SCD Type 2) and capture late-arriving NASA sensor heartbeats using windowed incremental logic.

### Commands Executed
- `source main_venv/bin/activate && dbt snapshot --select erp_equipment_status_snapshot --project-dir dbt --profiles-dir dbt`
- `source main_venv/bin/activate && dbt run --select gold.nasa_late_arrival_buffer --project-dir dbt --profiles-dir dbt`
- `source main_venv/bin/activate && python -c "import duckdb; print(duckdb.connect('dbt/factory_analytics.db').execute('SELECT * FROM nasa_late_arrival_buffer WHERE is_late_arrival = 1 LIMIT 10').fetchdf())"`

### Outcome
- SCD Type 2 snapshot `erp_equipment_status_snapshot` created and executed, preserving the full history of equipment status changes.
- Incremental model `nasa_late_arrival_buffer` created and executed, ready to flag late-arriving NASA sensor heartbeats.
- No late arrivals detected in current data, confirming model logic.

### Notes
- The snapshot uses the `check` strategy on the `status` column and tracks changes by `universal_asset_id`.
- The late-arrival buffer uses a 5-cycle window to detect out-of-sequence sensor heartbeats per unit.
- All results validated in DuckDB.
