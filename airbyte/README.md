# Airbyte Setup Instructions

This file documents the setup and configuration of Airbyte for syncing simulated ERP data (Postgres) and NASA sensor CSVs into the DuckDB Bronze layer.

---

## 1. Start Airbyte Locally (Docker Compose)

1. Clone the official Airbyte repo or use the Docker Compose quickstart:

   ```bash
   git clone https://github.com/airbytehq/airbyte.git
   cd airbyte
   docker compose up
   ```
   Or use the official quickstart script:
   ```bash
   curl -sL https://airbyte.io/install.sh | bash
   ./run-ab-platform.sh
   ```

2. Access the Airbyte UI at http://localhost:8000

---

## 2. Start Local Postgres (Docker Compose)

Add this service to your `.devcontainer/docker-compose.yml`:

```yaml
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: airbyte
      POSTGRES_PASSWORD: airbyte
      POSTGRES_DB: erp
    ports:
      - "5432:5432"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
```

Start/restart the stack:
```bash
docker compose -f .devcontainer/docker-compose.yml up -d postgres
```

---

## 3. Load ERP Data into Postgres

1. Create a table and import the simulated ERP CSV:

   ```bash
   docker compose exec postgres psql -U airbyte -d erp -c "\
   CREATE TABLE IF NOT EXISTS maintenance_logs (
     datum TEXT,
     anlage TEXT,
     standort TEXT,
     status TEXT,
     kosten_eur TEXT
   );"

   docker compose exec -T postgres psql -U airbyte -d erp -c "\
   COPY maintenance_logs FROM PROGRAM 'iconv -f ISO-8859-1 -t UTF-8 /var/lib/postgresql/data/erp_maintenance_logs.csv' DELIMITER ';' CSV HEADER;"
   ```
   (Ensure the CSV is available in the mapped volume: `./data/postgres/erp_maintenance_logs.csv`)

---

## 4. Airbyte Connections

- **Source 1:** Postgres (localhost:5432, db: erp, user: airbyte, password: airbyte)
- **Source 2:** NASA sensor CSVs (local CSV directory: `data/raw/sensors/`)
- **Destination:** DuckDB (file: `dbt/factory_analytics.db`)

Configure these in the Airbyte UI:
- Add Postgres source, select `maintenance_logs` table.
- Add CSV source, point to NASA sensor files.
- Add DuckDB destination, set path to `dbt/factory_analytics.db`.
- Create connections to sync both sources into the Bronze schema.

---

## 5. Run and Validate

- Trigger sync jobs in Airbyte UI.
- Validate data in DuckDB:
  ```sql
  SELECT * FROM bronze.maintenance_logs;
  SELECT * FROM bronze.nasa_sensors;
  ```

---

## 6. Troubleshooting
- Ensure all containers are running and ports are mapped.
- Check Airbyte and Postgres logs for errors.
- Confirm file encodings and volume mounts.
