# Batch 1.1: Environment & Secret Management (2026-04-12)

## Objective: Set up reproducible Codespace, secrets, orchestration, and DuckDB

### Codespace Orchestration
- mkdir -p .devcontainer
- touch .devcontainer/devcontainer.json .devcontainer/Dockerfile

### Secure Credentials
- (Manual) Add KAGGLE_USERNAME and KAGGLE_KEY to GitHub Codespaces secrets

### Orchestration Setup
- make up
- make down
- make status

### DuckDB Persistence
- python3 scripts/init_duckdb.py  # (if used for DB init)

### Git Operations
- git add .devcontainer/ airflow/ dbt/ scripts/ docs/command/bash-shell-commands.md docs/command/git-commands.md docs/governance/project-runbook.md docs/phase-reports/phase-1/phase-1-ingestion-report.md
- git commit -m "env+infra: complete Batch 1.1 (Codespace, Airflow, DuckDB, secrets)"
- git push origin master

# Phase 1 Ingestion Commands

Log all commands specific to Phase 1 (Ingestion) here.

# 2026-04-13: Batch 1.2 - Dual Intake Pipeline (Native Ingestion)

## Objective: Ingest NASA IoT and German ERP data into DuckDB (Bronze Layer)

### Step 1: Download NASA Turbofan Data
- Command: bash scripts/download_nasa_turbofan.sh
- Outcome: NASA Turbofan Failure Data downloaded and extracted to data/raw/sensors/

### Step 2: Generate German ERP Logs
- Command: python3 scripts/generate_german_erp.py
- Outcome: ERP maintenance logs generated in data/raw/erp_maintenance_logs.csv (ISO-8859-1, German format)

### Step 3: Ingest ERP Logs into DuckDB
- Command: python3 scripts/ingest_erp_to_duckdb.py
- Outcome: ERP maintenance logs ingested into DuckDB table 'bronze_erp_maintenance_logs'

### Step 4: Ingest NASA Sensor Data into DuckDB
- Command: python3 scripts/ingest_nasa_to_duckdb.py
- Outcome: NASA Turbofan train/test data ingested into DuckDB tables 'bronze_nasa_train', 'bronze_nasa_test'

### Step 5: Run All Ingestion Scripts (Batch)
- Command: bash scripts/run_all.sh
- Outcome: All ingestion scripts completed. Data loaded into DuckDB.
