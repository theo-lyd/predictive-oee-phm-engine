# Metabase OEE Dashboard Automation Script

# This script provides SQL and step-by-step instructions to automate the creation of a high-level OEE dashboard in Metabase after initial setup.

---

## 1. Add DuckDB Database in Metabase
- Go to **Admin > Databases > Add Database**
- Select **DuckDB**
- File path: `/workspaces/predictive-oee-phm-engine/dbt/factory_analytics.db`

---

## 2. Create OEE Trend Question (SQL)
- Click **New > SQL Question**
- Select your DuckDB database
- Paste the following SQL:

```sql
SELECT unit_number, oee, availability, performance, quality
FROM oee_final
ORDER BY unit_number
```

- Click **Visualize**
- Choose **Line** or **Bar** chart
  - X-axis: `unit_number`
  - Y-axis: `oee`
- Click **Save** and name it (e.g., `OEE by Asset`)

---

## 3. Add More Visualizations
- For RUL:

```sql
SELECT unit_number, avg_rul_pred FROM nasa_rul_regressor ORDER BY unit_number
```

- For FHI:

```sql
SELECT unit_number, factory_health_index FROM factory_health_index ORDER BY unit_number
```

- Visualize as needed and save each question.

---

## 4. Build the Dashboard
- Click **New > Dashboard**
- Name it (e.g., `Factory OEE & Health`)
- Add your saved questions (OEE, RUL, FHI, etc.)
- Arrange and resize as desired
- (Optional) Add filters for unit_number, date, etc.

---

## 5. Example Layout
- **OEE by Asset** (bar/line chart)
- **RUL by Asset** (bar/line chart)
- **Factory Health Index** (bar/line chart)
- (Optional) Add tables for detailed metrics

---

## 6. Save and Share
- Save the dashboard
- Share the link or export as needed

---

## 7. Troubleshooting
- If you don't see DuckDB as an option, ensure the JDBC driver is loaded and Metabase was restarted.
- If tables are missing, check that dbt models are built and the DuckDB file is up to date.

---

This script provides all SQL and steps needed for a high-level OEE dashboard in Metabase. For further automation (e.g., via Metabase API), let me know!