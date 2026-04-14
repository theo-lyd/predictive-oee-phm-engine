# Monte Carlo Lineage & IoT Heartbeat Monitoring (Phase 6)

This document describes the requirements and implementation plan for observability and monitoring in the predictive OEE PHM engine, as required by Phase 6.

## Goals
- **Data pipeline heartbeat:** Detect missing or delayed data in key DuckDB tables (OEE, sensor, ERP logs).
- **Lineage monitoring:** Track data flow from raw ingestion through dbt models to Gold layer outputs.
- **Alerting:** Notify stakeholders if data is missing, delayed, or if pipeline breaks are detected.
- **Extensibility:** Enable future integration with observability platforms (e.g., Monte Carlo, OpenLineage).

## Implementation
- A placeholder script is provided: `scripts/monte_carlo_heartbeat_monitor.py`
- The script outlines how to check for data arrival and log heartbeat events for key tables.
- Alerting and integration with external platforms are not yet implemented, but hooks are provided for future work.

## Usage
- Run the script manually or schedule it via cron/CI to simulate heartbeat checks.
- Extend the script to connect to DuckDB, query for recent data, and trigger alerts as needed.

## Next Steps
- Implement actual DuckDB queries for data freshness.
- Add alerting (email, Slack, etc.) for missing/stale data.
- Integrate with observability/lineage tools if/when available.

---

**Status:** Placeholder script and documentation provided. No active monitoring or alerting is currently running.
