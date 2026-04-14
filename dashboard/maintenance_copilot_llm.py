import streamlit as st
import duckdb
import pandas as pd
import openai
import os

st.set_page_config(page_title="Maintenance Copilot (LLM)", layout="wide")
st.title("🤖 Maintenance Copilot: Executive & Root-Cause Insights (LLM)")

# Helper to load tables
def get_table(query):
    con = duckdb.connect(database="../dbt/factory_analytics.db", read_only=True)
    df = con.execute(query).fetchdf()
    con.close()
    return df

# Load key marts
oee_df = get_table("SELECT * FROM oee_final ORDER BY unit_number")
fhi_df = get_table("SELECT * FROM factory_health_index ORDER BY unit_number")
rul_df = get_table("SELECT unit_number, avg(rul_pred) as avg_rul_pred FROM nasa_rul_regressor GROUP BY unit_number ORDER BY unit_number")
try:
    erp_df = get_table("SELECT * FROM erp_maintenance_normalized LIMIT 1000")
except Exception:
    erp_df = pd.DataFrame()

# Sidebar: Select asset/unit
default_unit = int(fhi_df['unit_number'].iloc[0]) if not fhi_df.empty else 1
unit = st.sidebar.number_input("Select Asset/Unit Number", min_value=1, max_value=int(fhi_df['unit_number'].max()), value=default_unit)

# Show summary metrics
st.header(f"Asset/Unit {unit} Health Overview")
row = fhi_df[fhi_df['unit_number'] == unit]
if not row.empty:
    st.metric("Factory Health Index (FHI)", f"{row['factory_health_index'].values[0]:.3f}")
    st.metric("OEE", f"{row['oee'].values[0]:.3f}")
    st.metric("Normalized RUL", f"{row['rul_normalized'].values[0]:.3f}")
else:
    st.warning("No data for selected unit.")

# Show OEE and RUL trend
st.subheader("OEE & RUL by Asset")
st.dataframe(oee_df.merge(rul_df, on="unit_number"), use_container_width=True)

# Show recent ERP maintenance logs (if available)
if not erp_df.empty:
    st.subheader("Recent Maintenance Logs (ERP)")
    st.dataframe(erp_df, use_container_width=True)

# LLM Context Synthesis
st.subheader("LLM Executive & Root-Cause Insights")
user_query = st.text_input("Ask a question about this asset (e.g., 'Why is Line 4 red?'):")

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_response = None
if user_query and openai_api_key:
    context = f"Asset/Unit: {unit}\nFHI: {row['factory_health_index'].values[0] if not row.empty else 'N/A'}\nOEE: {row['oee'].values[0] if not row.empty else 'N/A'}\nRUL: {row['rul_normalized'].values[0] if not row.empty else 'N/A'}\nRecent ERP logs: {erp_df.head(3).to_dict() if not erp_df.empty else 'N/A'}"
    prompt = f"You are a maintenance expert. Given the following context, answer the user's question.\nContext:\n{context}\n\nQuestion: {user_query}\nAnswer:"
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a maintenance expert."},
                      {"role": "user", "content": prompt}],
            max_tokens=256
        )
        llm_response = completion.choices[0].message.content
    except Exception as e:
        llm_response = f"[LLM Error] {e}"

if user_query:
    if openai_api_key:
        st.info(llm_response or "Waiting for LLM response...")
    else:
        st.warning("Set the OPENAI_API_KEY environment variable to enable LLM responses.")
else:
    st.caption("Type a question to get executive or root-cause insights.")

st.caption("Data source: DuckDB gold marts. LLM integration uses OpenAI GPT-3.5-turbo. Set OPENAI_API_KEY in your environment.")
