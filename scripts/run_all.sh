#!/bin/bash
# Run all ingestion scripts for Batch 1.2 (ERP and NASA to DuckDB)

set -e

# Activate main venv for Python scripts
source ../main_venv/bin/activate

# Ingest ERP logs
python3 ingest_erp_to_duckdb.py

# Ingest NASA sensor data
python3 ingest_nasa_to_duckdb.py

echo "All ingestion scripts completed. Data loaded into DuckDB."
