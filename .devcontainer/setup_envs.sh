#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Starting environment setup..."

WORKSPACE="/workspaces/predictive-oee-phm-engine"

# -------------------------------
# 1. Create Airflow-only venv
# -------------------------------
AIRFLOW_VENV="$WORKSPACE/airflow_venv"

if [ ! -d "$AIRFLOW_VENV" ]; then
    echo "📦 Creating Airflow virtual environment..."
    python3 -m venv "$AIRFLOW_VENV"
    source "$AIRFLOW_VENV/bin/activate"

    echo "⬆️ Upgrading pip..."
    pip install --upgrade pip

    echo "🌬️ Installing Apache Airflow (isolated)..."
    pip install "apache-airflow==2.8.1"

    deactivate
else
    echo "✔️ Airflow venv already exists, skipping creation."
fi


# -------------------------------
# 2. Create main environment venv
# -------------------------------
MAIN_VENV="$WORKSPACE/main_venv"

if [ ! -d "$MAIN_VENV" ]; then
    echo "📦 Creating main virtual environment..."
    python3 -m venv "$MAIN_VENV"
    source "$MAIN_VENV/bin/activate"

    echo "⬆️ Upgrading pip..."
    pip install --upgrade pip

    echo "📚 Installing dbt-core, DuckDB, Kaggle..."
    pip install \
        dbt-core \
        duckdb \
        duckdb-engine \
        kaggle

    deactivate
else
    echo "✔️ Main venv already exists, skipping creation."
fi


# -------------------------------
# 3. Summary
# -------------------------------
echo ""
echo "✅ All environments created successfully!"
echo ""
echo "To activate Airflow environment:"
echo "  source $AIRFLOW_VENV/bin/activate"
echo ""
echo "To activate main environment:"
echo "  source $MAIN_VENV/bin/activate"
echo ""
echo "🎉 Setup complete!"
