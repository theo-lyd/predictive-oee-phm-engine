# Airflow Commands Log

Append all Airflow-related commands here with timestamp, objective, command, and outcome.

## 2026-04-12: Batch 1.2 - NASA IoT Ingestion

### Objective: Register NASA Turbofan Ingestion DAG
- Command: cp scripts/download_nasa_turbofan.sh airflow/dags/ (referenced in DAG)
- Command: Created airflow/dags/nasa_turbofan_ingestion.py
- Outcome: DAG registered and visible in Airflow UI.

### Objective: Restart Airflow to register new DAG
- Command: docker compose -f .devcontainer/docker-compose.yml restart airflow
- Outcome: Airflow service restarted, DAG available for triggering.

### Objective: Trigger NASA Turbofan Ingestion DAG
- Command: (Manual) Triggered DAG 'nasa_turbofan_ingestion' via Airflow UI
- Outcome: NASA Turbofan Failure Data downloaded and extracted to data/raw/sensors/.
