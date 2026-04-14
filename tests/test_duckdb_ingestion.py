import os
import duckdb
import pandas as pd
import pytest

DB_PATH = "dbt/factory_analytics.db"


@pytest.fixture(scope="module")
def duckdb_conn():
    con = duckdb.connect(DB_PATH)
    yield con
    con.close()


def test_erp_table_exists(duckdb_conn):
    result = duckdb_conn.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'bronze_erp_maintenance_logs'"
    ).fetchone()
    assert result[0] == 1, "bronze_erp_maintenance_logs table should exist"


def test_nasa_train_table_exists(duckdb_conn):
    result = duckdb_conn.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'bronze_nasa_train'"
    ).fetchone()
    assert result[0] == 1, "bronze_nasa_train table should exist"


def test_nasa_test_table_exists(duckdb_conn):
    result = duckdb_conn.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'bronze_nasa_test'"
    ).fetchone()
    assert result[0] == 1, "bronze_nasa_test table should exist"


def test_erp_row_count(duckdb_conn):
    count = duckdb_conn.execute(
        "SELECT COUNT(*) FROM bronze_erp_maintenance_logs"
    ).fetchone()[0]
    assert count > 0, "ERP table should not be empty"


def test_nasa_train_row_count(duckdb_conn):
    count = duckdb_conn.execute("SELECT COUNT(*) FROM bronze_nasa_train").fetchone()[0]
    assert count > 0, "NASA train table should not be empty"


def test_nasa_test_row_count(duckdb_conn):
    count = duckdb_conn.execute("SELECT COUNT(*) FROM bronze_nasa_test").fetchone()[0]
    assert count > 0, "NASA test table should not be empty"
