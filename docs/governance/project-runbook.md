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