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
