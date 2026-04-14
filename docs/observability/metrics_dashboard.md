# Observability Metrics Dashboard (Concept)

This is a placeholder for a simple metrics dashboard. For production, integrate with Prometheus/Grafana or similar.

## Example Metrics (to be exposed by monitoring script):
- Last data timestamp for each monitored table
- Row counts for OEE, NASA Gold, Factory Health Index
- Number of stale data alerts in last 24h
- Last successful pipeline run time

## How to Use
- Extend `scripts/monte_carlo_heartbeat_monitor.py` to write metrics to a CSV, SQLite, or expose via HTTP (Flask/FastAPI).
- Visualize metrics with a simple dashboard or connect to Prometheus for scraping.

---

**Note:** For academic delivery, metrics are logged to stdout and can be redirected to a file for review.
