#!/usr/bin/env python3
"""
Ingest the simulated German ERP maintenance logs (ISO-8859-1, German format) into DuckDB (Bronze layer).
- Reads data/raw/erp_maintenance_logs.csv
- Writes to DuckDB table: bronze_erp_maintenance_logs
"""

import duckdb
import pandas as pd
import os
import sys

DUCKDB_PATH = "dbt/factory_analytics.db"
CSV_PATH = "data/raw/erp_maintenance_logs.csv"
TABLE_NAME = "bronze_erp_maintenance_logs"

def main():
	try:
		print(f"[INFO] Checking for ERP CSV at: {CSV_PATH}")
		if not os.path.exists(CSV_PATH):
			print(f"[ERROR] ERP CSV not found at {CSV_PATH}")
			sys.exit(1)
		print("[INFO] Reading ERP CSV...")
		erp_df = pd.read_csv(CSV_PATH, encoding="iso-8859-1", delimiter=";")
		print(f"[INFO] Read {len(erp_df)} rows from ERP CSV.")
		print(f"[INFO] Connecting to DuckDB at: {DUCKDB_PATH}")
		con = duckdb.connect(DUCKDB_PATH)
		print(f"[INFO] Dropping table if exists: {TABLE_NAME}")
		con.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
		print(f"[INFO] Creating table: {TABLE_NAME}")
		con.execute(f"CREATE TABLE {TABLE_NAME} AS SELECT * FROM erp_df")
		con.close()
		print(f"[SUCCESS] ERP maintenance logs ingested into DuckDB table '{TABLE_NAME}'")
	except Exception as e:
		print(f"[ERROR] Exception occurred: {e}")
		sys.exit(2)

if __name__ == "__main__":
	main()
