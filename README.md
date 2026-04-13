# predictive-oee-phm-engine

An Industry 4.0 predictive maintenance platform. Harmonizes NASA Turbofan IoT data with legacy ERP logs using a dbt-Databricks Medallion Architecture. Features RUL benchmarking, automated German market data normalization, and an LLM-powered "Maintenance Copilot" for prescriptive root-cause analysis.

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
