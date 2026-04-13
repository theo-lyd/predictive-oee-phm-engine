# ----------------------------------------
# Virtual Environment Shortcuts
# ----------------------------------------

AIRFLOW_VENV=./airflow_venv
MAIN_VENV=./main_venv

# Activate Airflow venv
airflow-env:
    @echo "🔄 Activating Airflow environment..."
    @echo "Run this in your terminal:"
    @echo ""
    @echo "    source $(AIRFLOW_VENV)/bin/activate"
    @echo ""

# Activate Main venv
main-env:
    @echo "🔄 Activating Main environment..."
    @echo "Run this in your terminal:"
    @echo ""
    @echo "    source $(MAIN_VENV)/bin/activate"
    @echo ""

# ----------------------------------------
# Airflow Commands
# ----------------------------------------

airflow-webserver:
    @echo "🚀 Starting Airflow Webserver (Airflow venv required)..."
    @$(AIRFLOW_VENV)/bin/airflow webserver

airflow-scheduler:
    @echo "📅 Starting Airflow Scheduler..."
    @$(AIRFLOW_VENV)/bin/airflow scheduler

airflow-init:
    @echo "🛠️ Initializing Airflow DB..."
    @$(AIRFLOW_VENV)/bin/airflow db init

# ----------------------------------------
# Makefile for Docker-like orchestration without Docker

.PHONY: up down status airflow dbt scripts

up: start

start:
	@echo "Starting all services..."
	bash ./start.sh

down: stop

stop:
	@echo "Stopping all services..."
	bash ./stop.sh

status:
	@echo "Service status:"
	bash ./status.sh

airflow:
	@echo "Starting Airflow..."
	cd airflow && source ../airflow_venv/bin/activate && airflow webserver -D && airflow scheduler -D

dbt:
	@echo "Running dbt..."
	cd dbt && dbt run

scripts:
	@echo "Running scripts..."
	cd scripts && bash ./run_all.sh
