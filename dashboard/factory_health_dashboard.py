import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Factory Health Dashboard", layout="wide")
st.title("🏭 Factory Health Index & Predictive Maintenance Dashboard")

# Connect to DuckDB and load tables
def get_table(query):
    con = duckdb.connect(database="../dbt/factory_analytics.db", read_only=True)
    df = con.execute(query).fetchdf()
    con.close()
    return df

# Load FHI, OEE, and RUL
fhi_df = get_table("SELECT * FROM factory_health_index ORDER BY unit_number")
oee_df = get_table("SELECT * FROM oee_final ORDER BY unit_number")
rul_df = get_table("SELECT unit_number, avg(rul_pred) as avg_rul_pred FROM nasa_rul_regressor GROUP BY unit_number ORDER BY unit_number")

st.header("Factory Health Index (FHI)")
st.dataframe(fhi_df, use_container_width=True)

st.header("OEE & RUL by Asset")
st.dataframe(oee_df.merge(rul_df, on="unit_number"), use_container_width=True)

st.header("FHI Distribution")
st.bar_chart(fhi_df.set_index("unit_number")["factory_health_index"])

st.header("OEE vs. Normalized RUL")
st.scatter_chart(fhi_df, x="oee", y="rul_normalized", color="factory_health_index", size="factory_health_index")

st.caption("Data source: DuckDB gold marts. For details, see docs/phase-reports/phase-5/factory_health_index.md.")
