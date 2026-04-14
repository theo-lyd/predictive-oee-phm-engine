import duckdb
import pathlib

db_path = pathlib.Path("dbt/factory_analytics.db")
db_path.parent.mkdir(exist_ok=True)
con = duckdb.connect(str(db_path))
con.execute(
    "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, note VARCHAR);"
)
con.close()
print(f"DuckDB database initialized at {db_path}")
