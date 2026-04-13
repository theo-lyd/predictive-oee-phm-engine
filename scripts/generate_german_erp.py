#!/usr/bin/env python3
"""
Generate simulated German ERP maintenance logs with:
- ISO-8859-1 encoding
- German numeric formats (e.g., 1.500,00)
- German status strings (e.g., 'Instandhaltung erforderlich')
- Factory locations with Umlaute (e.g., 'München', 'Göttingen')
"""
import csv
import random
from datetime import datetime, timedelta

# Output file
OUTPUT_FILE = "data/raw/erp_maintenance_logs.csv"

# German factory locations with Umlaute
FACTORIES = ["München", "Göttingen", "Düsseldorf", "Köln", "Leipzig"]

# German status strings
STATI = ["Instandhaltung erforderlich", "Wartung abgeschlossen", "Betrieb normal", "Störung erkannt"]

# Asset types
ASSETS = ["Motor", "Pumpe", "Kompressor", "Ventil"]

# Helper to format numbers in German style
format_german_number = lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Generate random ERP maintenance log entries
def generate_logs(num_records=100):
    logs = []
    start_date = datetime(2025, 1, 1)
    for i in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 365))
        asset = random.choice(ASSETS)
        factory = random.choice(FACTORIES)
        status = random.choice(STATI)
        cost = random.uniform(500, 5000)
        cost_str = format_german_number(cost)
        logs.append([
            date.strftime("%d.%m.%Y"),
            asset,
            factory,
            status,
            cost_str
        ])
    return logs

if __name__ == "__main__":
    logs = generate_logs(200)
    with open(OUTPUT_FILE, "w", encoding="iso-8859-1", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Datum", "Anlage", "Standort", "Status", "Kosten (EUR)"])
        writer.writerows(logs)
    print(f"Generated {len(logs)} ERP maintenance logs to {OUTPUT_FILE} (ISO-8859-1, German format)")
