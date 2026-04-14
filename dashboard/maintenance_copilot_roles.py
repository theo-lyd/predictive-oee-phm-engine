import streamlit as st
import duckdb
import pandas as pd
import openai
import os

st.set_page_config(page_title="Maintenance Copilot (LLM+Roles)", layout="wide")
st.title("🤖 Maintenance Copilot: Root-Cause Insights by Stakeholder Role")


# Helper to load tables
def get_table(query):
    con = duckdb.connect(database="dbt/factory_analytics.db", read_only=True)
    df = con.execute(query).fetchdf()
    con.close()
    return df


# Load key marts
oee_df = get_table("SELECT * FROM oee_final ORDER BY unit_number")
fhi_df = get_table("SELECT * FROM factory_health_index ORDER BY unit_number")
rul_df = get_table(
    "SELECT unit_number, avg(rul_pred) as avg_rul_pred FROM nasa_rul_regressor GROUP BY unit_number ORDER BY unit_number"
)
try:
    erp_df = get_table("SELECT * FROM erp_maintenance_normalized LIMIT 1000")
except Exception:
    erp_df = pd.DataFrame()


# Pre-populate defaults
default_unit = int(fhi_df["unit_number"].iloc[0]) if not fhi_df.empty else 1
default_role = "Maintenance Engineer"
default_question = f"Why is Line {default_unit} failing?"

# Demo mode configuration
DEMO_SCENARIOS = [
    {"role": "Maintenance Engineer", "question": "Why is Line 1 failing?"},
    {"role": "Factory Manager", "question": "What is the risk for Line 2?"},
    {"role": "Data Scientist", "question": "Explain the anomaly in Line 3."},
    {
        "role": "Quality Assurance",
        "question": "Are there any compliance issues for Line 4?",
    },
    {
        "role": "Operations Analyst",
        "question": "How can we improve throughput for Line 5?",
    },
]

# Demo mode state
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "demo_step" not in st.session_state:
    st.session_state.demo_step = 0

st.sidebar.markdown("---")
if st.sidebar.button("Run Demo Mode", key="demo_mode_btn"):
    st.session_state.demo_mode = True
    st.session_state.demo_step = 0

# Multi-asset selection
asset_options = list(fhi_df["unit_number"].unique()) if not fhi_df.empty else [1]
selected_assets = st.sidebar.multiselect(
    "Select Asset(s)/Unit(s) for Comparison",
    options=asset_options,
    default=[default_unit],
    key="asset_multiselect",
)

# Demo mode logic
roles_list = [
    "Maintenance Engineer",
    "Factory Manager",
    "Data Scientist",
    "Quality Assurance",
    "Operations Analyst",
]
if st.session_state.demo_mode:
    scenario = DEMO_SCENARIOS[st.session_state.demo_step % len(DEMO_SCENARIOS)]
    role = scenario["role"]
    demo_question = scenario["question"]
    # Cycle through assets for demo
    demo_unit = asset_options[st.session_state.demo_step % len(asset_options)]
    selected_assets = [demo_unit]
    st.sidebar.info(f"Demo Mode: {role} | Asset {demo_unit}")
    # Advance demo step on rerun
    st.session_state.demo_step += 1
    # Auto-stop after all scenarios
    if st.session_state.demo_step >= len(DEMO_SCENARIOS):
        st.session_state.demo_mode = False
else:
    role = st.sidebar.selectbox(
        "Simulate Stakeholder Role", roles_list, index=0, key="stakeholder_role"
    )
    demo_question = None

# Highlight assets with lowest FHI or RUL
highlight_n = 3
if not fhi_df.empty:
    fhi_sorted = fhi_df.sort_values("factory_health_index")
    low_fhi_assets = fhi_sorted.head(highlight_n)["unit_number"].tolist()
    rul_sorted = fhi_df.sort_values("rul_normalized")
    low_rul_assets = rul_sorted.head(highlight_n)["unit_number"].tolist()
    st.sidebar.markdown(f"**Assets with lowest FHI:** {low_fhi_assets}")
    st.sidebar.markdown(f"**Assets with lowest RUL:** {low_rul_assets}")

# Use first selected asset for single-asset LLM
unit = selected_assets[0] if selected_assets else default_unit


# Multi-asset comparison table
st.header("Asset Health Overview")
if selected_assets:
    compare_df = fhi_df[fhi_df["unit_number"].isin(selected_assets)].copy()
    compare_df = compare_df.merge(rul_df, on="unit_number", how="left")
    st.dataframe(compare_df, use_container_width=True)
else:
    st.warning("No assets selected.")


# Show OEE and RUL trend for all assets
st.subheader("OEE & RUL by Asset")
trend_df = oee_df.merge(rul_df, on="unit_number")
st.dataframe(trend_df, use_container_width=True)


# Show recent ERP maintenance logs (if available)
if not erp_df.empty:
    st.subheader("Recent Maintenance Logs (ERP)")
    st.dataframe(erp_df, use_container_width=True)


# LLM Context Synthesis with Role Simulation
st.subheader(f"LLM Root-Cause Insights ({role})")
if st.session_state.demo_mode and demo_question:
    user_query = demo_question
    st.info(f"[Demo] {user_query}")
else:
    user_query = st.text_input(
        "Ask a root-cause question about this asset (e.g., 'Why is Line 4 failing?'):",
        value=default_question,
        key="root_cause_question",
    )

# Role-specific prompt templates
role_templates = {
    "Maintenance Engineer": "You are a Maintenance Engineer. Focus on technical root causes, sensor anomalies, and actionable next steps.",
    "Factory Manager": "You are a Factory Manager. Focus on operational impact, downtime risk, and summary recommendations.",
    "Data Scientist": "You are a Data Scientist. Focus on data patterns, model predictions, and explainability.",
    "Quality Assurance": "You are in Quality Assurance. Focus on quality metrics, compliance, and defect trends.",
    "Operations Analyst": "You are an Operations Analyst. Focus on process efficiency, bottlenecks, and improvement opportunities.",
}

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_response = None
llm_prompt = ""
row = fhi_df[fhi_df["unit_number"] == unit]
if user_query and openai_api_key:
    context = f"Asset/Unit: {unit}\nFHI: {row['factory_health_index'].values[0] if not row.empty else 'N/A'}\nOEE: {row['oee'].values[0] if not row.empty else 'N/A'}\nRUL: {row['rul_normalized'].values[0] if not row.empty else 'N/A'}\nRecent ERP logs: {erp_df.head(3).to_dict() if not erp_df.empty else 'N/A'}"
    system_prompt = role_templates.get(
        role,
        f"You are a {role} at a factory. Answer root-cause questions with actionable, role-specific insights.",
    )
    llm_prompt = f"{system_prompt}\nGiven the following context, answer the user's root-cause question in a way that is actionable and relevant for your role.\nContext:\n{context}\n\nQuestion: {user_query}\nAnswer:"
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": llm_prompt},
            ],
            max_tokens=256,
        )
        llm_response = completion.choices[0].message.content
    except Exception as e:
        llm_response = f"[LLM Error] {e}"

if user_query:
    if openai_api_key:
        st.info(llm_response or "Waiting for LLM response...")
        # Show prompt transparency
        with st.expander("Show LLM Prompt/Context"):
            st.code(llm_prompt, language="markdown")
        # Downloadable report
        if llm_response:
            st.download_button(
                label="Download LLM Analysis as Text",
                data=f"Root-Cause Analysis for Asset {unit} ({role})\n\nQuestion: {user_query}\n\n{llm_response}",
                file_name=f"root_cause_analysis_unit{unit}_{role.replace(' ', '_')}.txt",
                mime="text/plain",
            )
    else:
        st.warning(
            "Set the OPENAI_API_KEY environment variable to enable LLM responses."
        )
else:
    st.caption("Type a root-cause question to get actionable, role-specific insights.")

st.caption(
    "Data source: DuckDB gold marts. LLM integration uses OpenAI GPT-3.5-turbo. Set OPENAI_API_KEY in your environment."
)
