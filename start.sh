#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting Predictive OEE PHM Engine..."

WORKSPACE="/workspaces/predictive-oee-phm-engine"
AIRFLOW_VENV="$WORKSPACE/airflow_venv"
MAIN_VENV="$WORKSPACE/main_venv"


# -------------------------------
# 1. Start Native Services
# -------------------------------
echo "🚦 Starting native services (no Docker)..."
echo "🗄️  Starting Postgres service..."
sudo service postgresql start

# -------------------------------
# 2. Initialize Airflow DB
# -------------------------------
echo "🛠️ Initializing Airflow metadata database..."
source "$AIRFLOW_VENV/bin/activate"
airflow db init

# -------------------------------
# 3. Start Airflow Webserver
# -------------------------------
echo "🌐 Starting Airflow Webserver..."
nohup airflow webserver > airflow_webserver.log 2>&1 &

# -------------------------------
# 4. Start Airflow Scheduler
# -------------------------------
echo "📅 Starting Airflow Scheduler..."
nohup airflow scheduler > airflow_scheduler.log 2>&1 &

deactivate

# -------------------------------
# 5. Validate dbt environment
# -------------------------------
echo "🔍 Running dbt debug..."
source "$MAIN_VENV/bin/activate"
dbt debug || echo "⚠️ dbt debug failed — check your profiles.yml"

deactivate

# -------------------------------
# 6. Summary
# -------------------------------
echo ""
echo "🎉 Predictive OEE PHM Engine is now running!"
echo ""
echo "Airflow Webserver: http://localhost:8080"
echo "Postgres: localhost:5432"
echo ""
echo "To view logs:"
echo "  tail -f airflow_webserver.log"
echo "  tail -f airflow_scheduler.log"
echo ""
echo "To stop everything:"
echo "  docker compose -f .devcontainer/docker-compose.yml down"
echo ""
