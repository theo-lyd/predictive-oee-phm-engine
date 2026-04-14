---

## 2026-04-12: Batch 1.2 - German ERP Simulation

### Scope
Simulate legacy German ERP maintenance logs with correct encoding, numeric formats, and Umlaute for ingestion pipeline testing.

### Steps
1. Created scripts/generate_german_erp.py to generate ERP logs with:
	- ISO-8859-1 encoding
	- German numeric formats (e.g., 1.500,00)
	- German status strings (e.g., 'Instandhaltung erforderlich')
	- Factory locations with Umlaute (e.g., 'München', 'Göttingen')
2. Ran the script to produce data/raw/erp_maintenance_logs.csv.
3. Verified encoding and format in the output file.

### Outcome
Simulated ERP logs are available for ingestion, with all German-specific requirements met.

# Project Runbook

Step-by-step reproduction guide for the project (native orchestration, no Docker or LFS).

---

## 2026-04-12: Batch 1.1 - Environment & Secret Management

### Scope
Establish reproducible developer environment, secure credentials, orchestrate Airflow, and initialize persistent DuckDB analytics database (all natively, no Docker/LFS).

### Steps
1. Created `.devcontainer` with `devcontainer.json` and `Dockerfile` to install dbt-core, Airflow, kaggle CLI, DuckDB CLI, and duckdb.
2. Added Codespaces secrets for `KAGGLE_USERNAME` and `KAGGLE_KEY`, mapped to environment and written to `~/.kaggle/kaggle.json`.
3. Set up Airflow, dbt, and Postgres as native services using Makefile and shell scripts (`start.sh`, `stop.sh`, `status.sh`).
4. Initialized persistent DuckDB database at `dbt/factory_analytics.db` and configured dbt profiles for local analytics.

### Outcome
All foundational infrastructure for ingestion and analytics is reproducible, secure, and ready for further pipeline development (no Docker or LFS required).

---

## 2026-04-12: Batch 1.2 - NASA IoT Ingestion

### Scope
Automate and document the ingestion of NASA Turbofan Failure Data using Airflow and the Kaggle CLI.

### Steps
1. Wrote Bash script (scripts/download_nasa_turbofan.sh) to download and extract NASA Turbofan data from Kaggle into data/raw/sensors/.
2. Created Airflow DAG (airflow/dags/nasa_turbofan_ingestion.py) to trigger the Bash script.
3. Restarted Airflow service to register the new DAG.
4. Manually triggered the DAG via Airflow UI to ingest data.
5. Verified all expected files in data/raw/sensors/.

### Outcome
NASA Turbofan Failure Data is reproducibly ingested and available for downstream processing. All steps are automated and auditable via Airflow and command logs.

---

## 2026-04-12: Batch Commit Correction & Traceability Enhancement

### Context
During implementation, a large batch of untracked files was mistakenly committed and pushed as a single commit, reducing traceability. This was corrected by:

1. Identifying the large batch commit and its parent.
2. Soft-resetting the branch to the previous commit, keeping all changes staged.
3. Recommitting changes in logical, smaller batches (data, architecture, business, command, etc.) with clear messages.
4. Force-pushing the improved commit history to the remote repository.

### Lessons Learned
- Always commit in logical, reviewable batches for traceability.
- Use clear, descriptive commit messages.
- Validate staged files before committing, especially when excluding sensitive or legacy content.
- Document all corrective actions in the runbook and command logs for full auditability.

---

## Troubleshooting & Recovery

### Common CI/CD Failures
- **SQL Linting Fails:**
  - Check SQLFluff output in GitHub Actions logs. Fix formatting and re-push.
- **Python Linting Fails:**
  - Run `black .`, `flake8 .`, and `mypy .` locally. Fix errors and re-push.
- **dbt Test Fails:**
  - Review which model/test failed in the logs. Validate data and model logic.
- **Artifact Upload Fails:**
  - Ensure `dbt/target/` exists after dbt run. Check workflow permissions.

### Monitoring/Observability Issues
- **Heartbeat Alerts:**
  - If you receive a stale data alert, check DuckDB for recent data ingestion.
  - If the script fails to connect, verify `dbt/factory_analytics.db` exists and is up to date.
- **Notification Failures:**
  - If Slack/email alerts are not received, check integration tokens and webhook URLs.

### General Recovery Steps
- Re-run failed workflow jobs after fixing issues.
- For persistent failures, consult the logs in `docs/command/` and escalate to the project maintainer.

---

## CI Optimization: Test Data Minimization & Resource Cleanup

- **Test Data Minimization:**
  - CI workflows use a small sample dataset for dbt and Python tests to ensure fast feedback.
  - Full data validation is run on scheduled builds or before production releases.
  - To customize, set the `SAMPLE_DATA` environment variable in CI and adjust scripts to use sample files.

- **Resource Cleanup:**
  - All temporary files, test artifacts, and intermediate outputs are deleted at the end of each CI run.
  - The CI workflow includes a `post-job` step to clean up the workspace and uploaded artifacts.

---

## Parallelization in CI/CD

- **Parallel Steps:**
  - Linting (SQL, Python) and dbt test jobs run in parallel to reduce total CI time.
  - dbt build and test can be parallelized using the `--threads` option (see `dbt_project.yml`).

- **Sample Data for CI:**
  - By default, CI runs on a reduced dataset for speed. Use the `SAMPLE_DATA` flag to switch between sample and full data.
  - For local testing, run `export SAMPLE_DATA=1` before executing scripts or dbt.

---

## CI/CD Pipeline Diagram

```mermaid
graph TD
    A[Code Push/PR] --> B[Lint SQL (SQLFluff)]
    A --> C[Lint Python (black/flake8/mypy)]
    B --> D[dbt Test (PR: modified, Main: all)]
    C --> D
    D --> E[Upload dbt Artifacts]
    D --> F[Fail Fast & Notify]
```

---

## Observability Playbook

### Alert Response Procedures
- **Stale Data Alert:**
  1. Check the DuckDB table and timestamp column flagged in the alert.
  2. Confirm recent data ingestion or pipeline run.
  3. If data is missing, trigger a manual ingestion or escalate.
- **Pipeline Exception:**
  1. Review error logs in the monitoring script and GitHub Actions.
  2. If a code or data bug, assign to engineering for fix.
  3. If an infrastructure issue, escalate to DevOps.

### Escalation Paths
- **First Response:** Project maintainer (see repo README)
- **Critical Failure:** Escalate to DevOps or academic supervisor
- **Notification Channels:** Slack/email (see notification integration in workflow/scripts)

---

# MSc Runbook: Predictive OEE PHM Engine (2026-04-14)

## Project Walkthrough

This runbook provides a step-by-step guide to the architecture, setup, and operation of the predictive OEE PHM engine. It is designed for MSc-level reproducibility and auditability.

### 1. Architecture Overview
- **Medallion Architecture:** Bronze (raw), Silver (cleaned), Gold (analytics)
- **Tech Stack:** DuckDB, dbt, Python, Great Expectations, Metabase, Streamlit
- **Key Features:**
  - German ERP and NASA IoT harmonization
  - In-warehouse ML (RUL, clustering)
  - LLM-powered Maintenance Copilot
  - CI/CD with GitHub Actions (Slim CI)
  - Observability (GE, Monte Carlo/heartbeat placeholder)

### 2. Setup & Installation
- Clone the repo and open in GitHub Codespaces or local dev environment
- Install Python 3.11+, dbt-core, dbt-duckdb, and dependencies
- See `.devcontainer/` for Codespace setup

### 3. Data Ingestion & Transformation
- Download NASA data: `bash scripts/download_nasa_turbofan.sh`
- Generate ERP logs: `python3 scripts/generate_german_erp.py`
- Ingest ERP logs: `python3 scripts/ingest_erp_to_duckdb.py`
- Ingest NASA data: `python3 scripts/ingest_nasa_to_duckdb.py`
- Run all: `bash scripts/run_all.sh`
- Build dbt models: `dbt run --project-dir dbt --profiles-dir dbt`

### 4. Data Quality & Governance
- Run Great Expectations suites: `python3 great_expectations/run_silver_suite.py`, `python3 great_expectations/run_gold_suite.py`
- All OEE and sensor data quality gates are validated
- See docs/phase-reports/ for validation logs

### 5. Analytics & ML
- Gold layer models: OEE, RUL, clustering
- Run ML models: `dbt run --select gold.nasa_rul_regressor --project-dir dbt --profiles-dir dbt`
- See docs/phase-reports/phase-4/ for ML tournament results

### 6. Executive Dashboards
- Streamlit Copilot: `python3 dashboard/maintenance_copilot_roles.py`
- Metabase: See docs/metabase_setup_no_docker.md and docs/metabase_dashboard_automation.md

### 7. CI/CD Pipeline
- GitHub Actions workflow: `.github/workflows/slim-ci-dbt-test.yml`
- On every PR, runs `dbt test` on modified models only
- Ensures "German Cleaning" logic is always validated

### 8. Observability & Monitoring
- Placeholder: `scripts/monte_carlo_heartbeat_monitor.py` for lineage/heartbeat
- See docs/monte_carlo_heartbeat_monitoring.md

### 9. Command Logs
- All commands and outcomes: `docs/command/`
- Git, Bash, dbt, Airflow, etc. for full reproducibility

### 10. Business Blueprint
- See `docs/business_blueprint.md` for business context and value

---

**For any issues, see the README and docs/ for troubleshooting and further details.**