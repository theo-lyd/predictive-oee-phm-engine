# DevContainer for Predictive OEE PHM Engine
FROM mcr.microsoft.com/devcontainers/python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --upgrade pip && \
    pip install dbt-core apache-airflow kaggle duckdb duckdb-engine

# Install DuckDB CLI
RUN curl -L https://github.com/duckdb/duckdb/releases/download/v0.10.2/duckdb_cli-linux-amd64.zip -o duckdb_cli.zip \
    && unzip duckdb_cli.zip -d /usr/local/bin \
    && mv /usr/local/bin/duckdb /usr/local/bin/duckdb_cli \
    && rm duckdb_cli.zip

# Set up environment variables for Airflow
ENV AIRFLOW_HOME=/workspace/airflow

# Default workdir
WORKDIR /workspaces/predictive-oee-phm-engine
