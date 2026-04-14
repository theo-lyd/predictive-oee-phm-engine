# predictive-oee-phm-engine


An Industry 4.0 predictive maintenance platform. Harmonizes NASA Turbofan IoT data with legacy ERP logs using a dbt-Databricks Medallion Architecture. Features:
- RUL benchmarking and robust ML tournament (Random Forest, Linear Regression, XGBoost) with advanced tuning, diagnostics, and explainability
- Automated German market data normalization
- KMeans anomaly segmentation with health zone profiling
- LLM-powered "Maintenance Copilot" for prescriptive root-cause analysis
- Full documentation of enhancements and results in phase reports

---

## Quick Reference Index

### 📁 docs/
- [Architecture](docs/architecture/README.md): Specifications, diagrams, and critiques
- [Business](docs/business/README.md): Blueprint, project brief, and business context
- [Command](docs/command/README.md): Command logs and reproducibility evidence
- [Data](docs/data/README.md): Data specifications, profiling, and critique
- [Governance](docs/governance/README.md): Execution governance and policies
- [Incidents](docs/incidents/README.md): Per-phase issue and incident logs
- [Phase Reports](docs/phase-reports/README.md): Batch and sprint execution reports
- [Planning](docs/planning/README.md): Backlog, sprints, and implementation plan
- [Security](docs/security/README.md): Security specifications and compliance
- [Specification](docs/specification/README.md): Requirements, architecture, data, interface, test, deployment, and governance specs

### Key Implementation & Planning Files
- [Implementation Plan](docs/planning/implementation_plan.md)
- [Project Runbook](docs/governance/project-runbook.md)
- [Repo Standing Instructions & Execution Governance](docs/governance/repo-standing-instructions-and-execution-governance.md)
- [Business Blueprint](docs/business/business_blueprint.md)
- [Project Details](docs/business/project_details.md)

### Command Reference (for reproducibility)
- [Git Commands](docs/command/git-commands.md)
- [Bash Shell Commands](docs/command/bash-shell-commands.md)
- [Airbyte Commands](docs/command/airbyte-commands.md)
- [Airflow Commands](docs/command/airflow-commands.md)
- [dbt Commands](docs/command/dbt-commands.md)
- [Docker Commands](docs/command/docker-commands.md)
- [DuckDB Commands](docs/command/duckdb-commands.md)
- [GitHub Actions Commands](docs/command/github-actions-commands.md)
- [Lint Commands](docs/command/lint-commands.md)
- [Make Commands](docs/command/make-commands.md)
- [Python Commands](docs/command/python-commands.md)

---


## Native Orchestration (No Docker, No LFS)

This project now uses a Makefile and shell scripts (`start.sh`, `stop.sh`, `status.sh`) to orchestrate Airflow, dbt, and Postgres natively. Docker and Git LFS have been fully removed for maximum compatibility with Codespaces and local Linux environments. All data is managed directly in the workspace (no LFS required).

### Quickstart
- `make up` – Start all services (Airflow, dbt, Postgres)
- `make down` – Stop all services
- `make status` – Show running services

**Note:** If you previously used Docker or Git LFS, please update your local clone and remove any LFS hooks/configs.

For a full project walkthrough, see the [Project Runbook](docs/governance/project-runbook.md) and [Implementation Plan](docs/planning/implementation_plan.md).

---

## Batch 1.2: Dual Intake Pipeline (Native Ingestion)

This project natively ingests both NASA Turbofan IoT data and simulated German ERP logs into DuckDB using Python and Bash scripts (no Airbyte, no Docker required).

### Ingestion Steps
1. Download NASA data: `bash scripts/download_nasa_turbofan.sh`
2. Generate ERP logs: `python3 scripts/generate_german_erp.py`
3. Ingest ERP logs: `python3 scripts/ingest_erp_to_duckdb.py`
4. Ingest NASA data: `python3 scripts/ingest_nasa_to_duckdb.py`
5. (Batch) Run all: `bash scripts/run_all.sh`

- All commands and outcomes are logged in [docs/command/](docs/command/) and [docs/phase-reports/phase-1/phase-1-ingestion-commands.md](docs/phase-reports/phase-1/phase-1-ingestion-commands.md)
- Airbyte has been fully replaced by native Python + dbt + DuckDB scripts for ingestion.

See [Implementation Plan](docs/planning/implementation_plan.md) for details.

---

## Factory Health Index (FHI)

A unified metric combining OEE and normalized RUL for each asset. See [phase-5/factory_health_index.md](docs/phase-reports/phase-5/factory_health_index.md) for definition and usage. Visualized in the dashboard and available in the gold layer as `factory_health_index`.

---

## 📊 Factory Health Dashboard

A Streamlit dashboard is available at `dashboard/factory_health_dashboard.py` to visualize:
- Factory Health Index (FHI)
- OEE and RUL by asset
- FHI distribution and OEE vs. normalized RUL

Run with:

```bash
streamlit run dashboard/factory_health_dashboard.py
```

See [phase-5/factory_health_index.md](docs/phase-reports/phase-5/factory_health_index.md) for metric details.

---

## 🤖 Maintenance Copilot Dashboard

A Streamlit app for executive and root-cause insights is available at `dashboard/maintenance_copilot.py`. It provides:
- Asset-level FHI, OEE, and RUL metrics
- Recent ERP maintenance logs
- LLM-style context synthesis and root-cause explanations (placeholder logic)

Run with:

```bash
streamlit run dashboard/maintenance_copilot.py
```

*LLM integration is a placeholder; see code for extension points.*

---

## 🤖 Maintenance Copilot (LLM) Dashboard

A Streamlit app with real LLM integration is available at `dashboard/maintenance_copilot_llm.py`. It provides:
- Asset-level FHI, OEE, and RUL metrics
- Recent ERP maintenance logs
- Executive and root-cause insights powered by OpenAI GPT-3.5-turbo

**Usage:**
1. Set your OpenAI API key in the environment: `export OPENAI_API_KEY=sk-...`
2. Run:
   ```bash
   streamlit run dashboard/maintenance_copilot_llm.py
   ```

*If no API key is set, the app will prompt for it and fallback to placeholder logic.*

---

## 🤖 Maintenance Copilot (LLM+Roles) Dashboard

A Streamlit app for root-cause analysis with stakeholder role simulation is available at `dashboard/maintenance_copilot_roles.py`. It provides:
- Asset-level FHI, OEE, and RUL metrics
- Recent ERP maintenance logs
- LLM-powered root-cause answers tailored to simulated roles (Engineer, Manager, Data Scientist, QA, Analyst)

**Usage:**
1. Set your OpenAI API key in the environment: `export OPENAI_API_KEY=sk-...`
2. Run:
   ```bash
   streamlit run dashboard/maintenance_copilot_roles.py
   ```

*Select a stakeholder role in the sidebar to simulate different perspectives in root-cause analysis.*
