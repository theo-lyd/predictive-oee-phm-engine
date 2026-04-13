#!/usr/bin/env python3
"""
Ingest the simulated German ERP maintenance logs (ISO-8859-1, German format) into DuckDB (Bronze layer).
- Reads data/raw/erp_maintenance_logs.csv
- Writes to DuckDB table: bronze_erp_maintenance_logs
"""
import duckdb
import pandas as pd

DUCKDB_PATH = "dbt/factory_analytics.db"
CSV_PATH = "data/raw/erp_maintenance_logs.csv"
TABLE_NAME = "bronze_erp_maintenance_logs"

# Read the ERP CSV with German encoding and delimiter
erp_df = pd.read_csv(CSV_PATH, encoding="iso-8859-1", delimiter=";")

# Connect to DuckDB and ingest
con = duckdb.connect(DUCKDB_PATH)
con.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
con.execute(f"CREATE TABLE {TABLE_NAME} AS SELECT * FROM erp_df")
con.close()
print(f"ERP maintenance logs ingested into DuckDB table '{TABLE_NAME}'")
