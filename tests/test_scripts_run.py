import subprocess
import os
import pytest

def test_generate_german_erp_runs():
    result = subprocess.run(["python3", "scripts/generate_german_erp.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert os.path.exists("data/raw/erp_maintenance_logs.csv"), "ERP log file not created"

def test_ingest_erp_to_duckdb_runs():
    result = subprocess.run(["python3", "scripts/ingest_erp_to_duckdb.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed: {result.stderr}"

def test_ingest_nasa_to_duckdb_runs():
    result = subprocess.run(["python3", "scripts/ingest_nasa_to_duckdb.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed: {result.stderr}"
