"""
monte_carlo_heartbeat_monitor.py

This script is a placeholder for implementing Monte Carlo lineage monitoring and IoT Heartbeat alerting for the predictive OEE PHM engine.

Features to implement:
- Data pipeline heartbeat: Periodically check for data arrival in DuckDB tables (e.g., OEE, sensor, ERP logs).
- Lineage monitoring: Track and log the flow of data from raw ingestion through dbt models to Gold layer outputs.
- Alerting: Send alerts (e.g., email, Slack, log) if data is missing, delayed, or if pipeline breaks are detected.
- Extensible: Integrate with observability platforms (e.g., Monte Carlo, OpenLineage) if/when available.

Current status: Not implemented. This file serves as a template and documentation anchor for Phase 6 observability requirements.
"""

import time
import logging
from datetime import datetime, timedelta
import duckdb
import os
import smtplib
from email.message import EmailMessage
import requests
import csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

MONITORED_TABLES = {
    "oee_final": "unit_number",
    "nasa_gold": "sensor_timestamp",
    "factory_health_index": "unit_number",
}

DUCKDB_PATH = os.getenv(
    "DUCKDB_PATH", "/workspaces/predictive-oee-phm-engine/dbt/factory_analytics.db"
)
STALE_THRESHOLD_MINUTES = 15
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

METRICS_CSV = os.getenv(
    "METRICS_CSV", "/workspaces/predictive-oee-phm-engine/monitoring_metrics.csv"
)


def send_slack_alert(message):
    if SLACK_WEBHOOK_URL:
        try:
            requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        except Exception as e:
            logging.error(f"Slack alert failed: {e}")


def send_email_alert(subject, body):
    if ALERT_EMAIL and SMTP_SERVER and SMTP_USER and SMTP_PASS:
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = SMTP_USER
            msg["To"] = ALERT_EMAIL
            with smtplib.SMTP_SSL(SMTP_SERVER) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Email alert failed: {e}")


def send_alert(table, message):
    alert_msg = f"ALERT: {table}: {message}"
    logging.error(alert_msg)
    send_slack_alert(alert_msg)
    send_email_alert(f"[OEE PHM ALERT] {table}", alert_msg)


def check_table_heartbeat(con, table_name, ts_col, metrics):
    try:
        if ts_col == "unit_number":
            result = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            row_count = result[0]
            logging.info(f"[HEARTBEAT] {table_name}: row count = {row_count}")
            metrics.append(
                {
                    "table": table_name,
                    "metric": "row_count",
                    "value": row_count,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            if row_count == 0:
                send_alert(table_name, "No rows found!")
        else:
            result = con.execute(f"SELECT MAX({ts_col}) FROM {table_name}").fetchone()
            latest_ts = result[0]
            logging.info(f"[HEARTBEAT] {table_name}: latest {ts_col} = {latest_ts}")
            metrics.append(
                {
                    "table": table_name,
                    "metric": f"latest_{ts_col}",
                    "value": latest_ts,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            if latest_ts is None:
                send_alert(table_name, "No data found!")
            elif isinstance(latest_ts, int) and latest_ts < 1:
                send_alert(table_name, f"Stale data: latest {ts_col} = {latest_ts}")
    except Exception as e:
        send_alert(table_name, f"Exception: {e}")


def write_metrics_csv(metrics):
    with open(METRICS_CSV, "w", newline="") as csvfile:
        fieldnames = ["table", "metric", "value", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in metrics:
            writer.writerow(row)


def main():
    logging.info("Starting Monte Carlo/Heartbeat monitor (production)")
    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    metrics = []
    for table, ts_col in MONITORED_TABLES.items():
        check_table_heartbeat(con, table, ts_col, metrics)
    con.close()
    write_metrics_csv(metrics)
    logging.info("Monitoring complete.")


if __name__ == "__main__":
    main()
