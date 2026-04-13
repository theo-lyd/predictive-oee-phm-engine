#!/bin/bash
set -e

echo "[status.sh] Airflow processes:"
ps aux | grep '[a]irflow'

echo "[status.sh] dbt processes:"
ps aux | grep '[d]bt'

echo "[status.sh] Script processes:"
ps aux | grep '[g]enerate_german_erp.py\|[d]ownload_nasa_turbofan.sh\|[i]nit_duckdb.py'

echo "[status.sh] Postgres service status:"
sudo service postgresql status | grep Active
