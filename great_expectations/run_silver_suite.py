import duckdb
import pandas as pd
import great_expectations.expectations as exp


def run_integrity_checks():
    con = duckdb.connect("dbt/factory_analytics.db")
    df = con.execute("SELECT * FROM nasa_silver").df()
    results = []
    # Check if 'quality' column exists
    if "quality" in df.columns:
        col = df["quality"]
        in_range = col.between(0.0, 1.0).all()
        results.append(
            {
                "expectation": "expect_column_values_to_be_between",
                "success": in_range,
                "result": (
                    "All values between 0 and 1"
                    if in_range
                    else "Some values out of range"
                ),
            }
        )
    else:
        results.append(
            {
                "expectation": "expect_column_values_to_be_between",
                "success": False,
                "result": 'Column "quality" not found.',
            }
        )

    # Check if 'sensor_timestamp' column exists
    if "sensor_timestamp" in df.columns and "unit_number" in df.columns:
        # Check monotonicity within each unit_number
        monotonic = (
            df.groupby("unit_number")["sensor_timestamp"]
            .apply(lambda x: x.is_monotonic_increasing)
            .all()
        )
        results.append(
            {
                "expectation": "expect_column_values_to_be_increasing",
                "success": monotonic,
                "result": (
                    "Monotonic per unit_number"
                    if monotonic
                    else "Not monotonic per unit_number"
                ),
            }
        )
    else:
        results.append(
            {
                "expectation": "expect_column_values_to_be_increasing",
                "success": False,
                "result": 'Column "sensor_timestamp" or "unit_number" not found.',
            }
        )
    return results


if __name__ == "__main__":
    results = run_integrity_checks()
    for r in results:
        print(r)
