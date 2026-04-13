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
