from sqlalchemy import create_engine, text
import os
import pandas as pd

# DuckDB connection
engine = create_engine('duckdb:///dbt/factory_analytics.db')

# Query data from nasa_gold
with engine.connect() as conn:
    result = conn.execute(text("SELECT unit_number, sensor_timestamp, quality FROM nasa_gold ORDER BY unit_number, sensor_timestamp"))
    rows = result.fetchall()

# Convert to pandas DataFrame
df = pd.DataFrame(rows, columns=["unit_number", "sensor_timestamp", "quality"])

# Run expectations
results = {}
results['quality'] = df["quality"].between(0, 1).all()
results['monotonic'] = df.groupby("unit_number")["sensor_timestamp"].apply(lambda x: x.is_monotonic_increasing).all()

print('Quality expectation:', results['quality'])
print('Monotonic timestamp expectation:', results['monotonic'])

# Save results
os.makedirs('great_expectations/validation_definitions', exist_ok=True)
with open('great_expectations/validation_definitions/gold_suite_results.txt', 'w') as f:
    f.write(f"Quality expectation: {results['quality']}\n")
    f.write(f"Monotonic timestamp expectation: {results['monotonic']}\n")
