#!/usr/bin/env python3
"""
Ingest NASA Turbofan sensor data (all train/test files) into DuckDB (Bronze layer).
- Reads all data/raw/sensors/train_FD*.txt and test_FD*.txt
- Writes to DuckDB tables: bronze_nasa_train, bronze_nasa_test
"""

import duckdb
import pandas as pd
import glob

DUCKDB_PATH = "dbt/factory_analytics.db"
SENSORS_DIR = "data/raw/sensors"

# NASA file patterns
TRAIN_PATTERN = f"{SENSORS_DIR}/train_FD*.txt"
TEST_PATTERN = f"{SENSORS_DIR}/test_FD*.txt"

# Helper to load and concatenate all files


def load_nasa_files(pattern):
    dfs = []
    for file in glob.glob(pattern):
        df = pd.read_csv(file, delim_whitespace=True, header=None)
        df["source_file"] = file.split("/")[-1]
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


# Ingest train files
train_df = load_nasa_files(TRAIN_PATTERN)
# Ingest test files
test_df = load_nasa_files(TEST_PATTERN)

con = duckdb.connect(DUCKDB_PATH)
con.execute("DROP TABLE IF EXISTS bronze_nasa_train_physical")
con.execute("DROP TABLE IF EXISTS bronze_nasa_test_physical")
con.execute("CREATE TABLE bronze_nasa_train_physical AS SELECT * FROM train_df")
con.execute("CREATE TABLE bronze_nasa_test_physical AS SELECT * FROM test_df")
con.close()
print(
    "NASA Turbofan train/test data ingested into DuckDB (bronze_nasa_train, bronze_nasa_test)"
)
