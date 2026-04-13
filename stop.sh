#!/bin/bash
set -e

echo "[stop.sh] Stopping Airflow webserver and scheduler..."
# Find and kill Airflow processes
pkill -f 'airflow webserver' || true
pkill -f 'airflow scheduler' || true

echo "[stop.sh] No persistent dbt or script processes to stop."
echo "[stop.sh] All services stopped."
