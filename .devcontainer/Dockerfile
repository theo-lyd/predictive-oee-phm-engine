# DevContainer for Predictive OEE PHM Engine
FROM mcr.microsoft.com/devcontainers/python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    unzip \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*


# Install DuckDB CLI
RUN curl -L https://github.com/duckdb/duckdb/releases/download/v0.10.2/duckdb_cli-linux-amd64.zip -o duckdb_cli.zip \
    && unzip duckdb_cli.zip -d /usr/local/bin \
    && mv /usr/local/bin/duckdb /usr/local/bin/duckdb_cli \
    && rm duckdb_cli.zip

WORKDIR /workspaces/predictive-oee-phm-engine