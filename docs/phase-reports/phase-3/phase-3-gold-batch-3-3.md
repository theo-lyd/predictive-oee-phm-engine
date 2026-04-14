# Batch 3.3: Integrity & Logic Contracts (Gold Layer)

## Objective
Implement data integrity and logic contracts at the Gold boundary using Great Expectations (GE) to ensure:
- All "quality" scores are between 0 and 1 (inclusive)
- All "sensor_timestamp" values are strictly increasing per unit (engine)

## Implementation Steps
1. **Gold Model Creation:**
   - Created `dbt/models/gold/nasa_gold.sql` to expose `unit_number`, `cycle` (as `sensor_timestamp`), and min-max normalized `quality` (sensor 6) per unit.
   - Used the same column extraction logic as the Silver layer to ensure correct schema.
2. **Model Build:**
   - Ran `dbt run --select gold.nasa_gold` to build the model in DuckDB.
3. **Validation Suite:**
   - Implemented `great_expectations/run_gold_suite.py` to validate:
     - All `quality` values are in [0, 1]
     - All `sensor_timestamp` values are strictly increasing per unit
   - Used pandas and DuckDB SQLAlchemy engine for direct validation.
   - Ran the suite and confirmed both expectations pass.

## Results
- `nasa_gold` table created and validated in DuckDB.
- All "quality" values are between 0 and 1; all "sensor_timestamp" values are strictly increasing per unit.
- Batch 3.3 requirements are fully met and contract-compliant.

## Commands Executed
- `dbt run --select gold.nasa_gold --project-dir dbt --profiles-dir dbt`
- `python3 great_expectations/run_gold_suite.py`

## Validation Output
```
Quality expectation: True
Monotonic timestamp expectation: True
```

---
Batch 3.3 is complete, validated, and documented.
