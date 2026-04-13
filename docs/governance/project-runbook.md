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

Step-by-step reproduction guide for the project.

---

## 2026-04-12: Batch 1.1 - Environment & Secret Management

### Scope
Establish reproducible developer environment, secure credentials, orchestrate Airflow, and initialize persistent DuckDB analytics database.

### Steps
1. Created `.devcontainer` with `devcontainer.json` and `Dockerfile` to install dbt-core, Airflow, kaggle CLI, DuckDB CLI, and duckdb.
2. Added Codespaces secrets for `KAGGLE_USERNAME` and `KAGGLE_KEY`, mapped to environment and written to `~/.kaggle/kaggle.json`.
3. Set up Airflow as a Docker service with SCRIPTS_DIR and DBT_DIR mapped for orchestration.
4. Initialized persistent DuckDB database at `dbt/factory_analytics.db` and configured dbt profiles for local analytics.

### Outcome
All foundational infrastructure for ingestion and analytics is reproducible, secure, and ready for further pipeline development.

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