# Metabase Setup for OEE Trend Visualization (No Docker)

This guide will help you install and configure Metabase to connect to your DuckDB file (`dbt/factory_analytics.db`) and create a high-level OEE trend dashboard.

---

## 1. Install Metabase (JAR Method)

1. Download the latest Metabase JAR:
   ```sh
   wget https://downloads.metabase.com/v0.50.9/metabase.jar -O metabase.jar
   ```
2. (Optional) Install Java if not present:
   ```sh
   sudo apt-get update && sudo apt-get install -y default-jre
   ```

---

## 2. Download DuckDB JDBC Driver

1. Download the DuckDB JDBC driver:
   ```sh
   wget https://repo1.maven.org/maven2/org/duckdb/duckdb_jdbc/0.10.2/duckdb_jdbc-0.10.2.jar -O duckdb_jdbc.jar
   ```
2. Place `duckdb_jdbc.jar` in the same directory as `metabase.jar`.

---

## 3. Start Metabase with DuckDB Driver

1. Set the `MB_PLUGINS_DIR` environment variable to the current directory:
   ```sh
   export MB_PLUGINS_DIR=$(pwd)
   ```
2. Start Metabase:
   ```sh
   java -jar metabase.jar
   ```
3. Open your browser and go to: http://localhost:3000

---

## 4. Connect DuckDB Database in Metabase

1. In Metabase, go to **Admin > Databases > Add Database**.
2. Select **DuckDB** as the database type.
3. For the file path, enter the absolute path to your DuckDB file, e.g.:
   ```
   /workspaces/predictive-oee-phm-engine/dbt/factory_analytics.db
   ```
4. Save the connection.

---

## 5. Create OEE Trend Dashboard

1. Click **New > Dashboard** and name it (e.g., "OEE Trends").
2. Click **New > SQL Question** and select your DuckDB database.
3. Use this sample query:
   ```sql
   SELECT unit_number, oee, availability, performance, quality
   FROM oee_final
   ORDER BY unit_number
   ```
4. Visualize as a line or bar chart (choose "unit_number" as X-axis, "oee" as Y-axis).
5. Save the question and add it to your dashboard.

---

## 6. (Optional) Add More Visualizations
- Add questions for RUL, FHI, or other metrics as needed.
- Use Metabase's filters and visualization options for deeper insights.

---

## 7. Stop Metabase
- Press `Ctrl+C` in the terminal running Metabase to stop the server.

---

## Troubleshooting
- If DuckDB is not available as a database type, ensure the JDBC JAR is in the plugins directory and restart Metabase.
- If you get file permission errors, check the path and permissions for `factory_analytics.db`.

---

## References
- [Metabase Documentation](https://www.metabase.com/docs/latest/)
- [DuckDB JDBC Driver](https://duckdb.org/docs/api/java.html)

---

This guide enables you to visualize OEE and related metrics in Metabase without Docker, using your local DuckDB file.