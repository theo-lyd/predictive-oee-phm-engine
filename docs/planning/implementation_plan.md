This implementation plan is structured to follow the **Developer Inner Loop** philosophy, ensuring that your **GitHub Codespace** acts as the command center while your data warehouse (DuckDB or Snowflake) handles the heavy lifting. Each phase is broken down into **Batches** (scope) and **Chunks** (atomic tasks) to ensure a systematic, thesis-level delivery.

---

# Phase 1: Foundation & Resilient Ingestion
**Goal:** Establish the infrastructure and automate the retrieval of multi-modal data.


### Batch 1.1: Environment & Secret Management
* **Chunk 1: Codespace Orchestration:** Configure `.devcontainer` to install `dbt-core`, `airflow`, `kaggle CLI`, DuckDB CLI, and `duckdb`.
* **Chunk 2: Secure Credentials:** Inject `KAGGLE_USERNAME` and `KAGGLE_KEY` into GitHub Secrets. Map them to the Codespace environment.
* **Chunk 3: Orchestration Setup:** Use Makefile and shell scripts to launch Airflow, dbt, and Postgres as native services (no Docker required). Define the SCRIPTS_DIR for Python ingestion and DBT_DIR for transformations.
* **Chunk 4: DuckDB Persistence:** Initialize factory_analytics.db. Configure dbt profiles to point to this local file, ensuring it is mounted to a persistent volume.


### Batch 1.2: Dual Intake Pipeline (Native Ingestion)

### What was implemented:
* Bash script to download NASA Turbofan Failure Data via Kaggle CLI (scripts/download_nasa_turbofan.sh)
* Python script to generate German ERP logs in ISO-8859-1 with German formats (scripts/generate_german_erp.py)
* Python script to ingest ERP logs into DuckDB (scripts/ingest_erp_to_duckdb.py)
* Python script to ingest NASA sensor data into DuckDB (scripts/ingest_nasa_to_duckdb.py)
* Batch runner script to execute all ingestion steps (scripts/run_all.sh)
* All commands and outcomes logged in docs/command/* and docs/phase-reports/phase-1/phase-1-ingestion-commands.md
* Airbyte replaced by native Python + dbt + DuckDB scripts for ingestion (no Airbyte required)

### How to run the full pipeline:
1. Download NASA data: `bash scripts/download_nasa_turbofan.sh`
2. Generate ERP logs: `python3 scripts/generate_german_erp.py`
3. Ingest ERP logs: `python3 scripts/ingest_erp_to_duckdb.py`
4. Ingest NASA data: `python3 scripts/ingest_nasa_to_duckdb.py`
5. (Batch) Run all: `bash scripts/run_all.sh`

### Where to find the data:
* NASA sensor files: data/raw/sensors/
* ERP logs: data/raw/erp_maintenance_logs.csv
* DuckDB tables: bronze_erp_maintenance_logs, bronze_nasa_train, bronze_nasa_test (in dbt/factory_analytics.db)

### Where to find the logs:
* Command logs: docs/command/
* Phase 1 ingestion log: docs/phase-reports/phase-1/phase-1-ingestion-commands.md

### Airbyte replacement:
* All ingestion is now handled natively via Python scripts and dbt. No Airbyte or Docker required.

---

# Phase 2: The "German" Data Refinery (Silver Layer)
**Goal:** Neutralize data "noise", harmonize disparate sources, and solve the German encoding/normalization challenges. 

### Batch 2.1: Encoding & String Normalization and Character Mapping
* **Chunk 1: The Encoding Shield:** Create a dbt macro to cast the raw ERP strings from `ISO-8859-1` to `UTF-8`. Encoding Shield: Develop dbt models that cast ISO-8859-1 raw strings into clean UTF-8
* **Chunk 2: Umlaut & Abbreviation Logic:** Write SQL regex patterns to replace Umlaute (e.g., `Lagerstörung` $\rightarrow$ `Lagerstoerung`) and expand shorthand (e.g., `Prüf.` $\rightarrow$ `Pruefung`). Create a dbt macro to map German characters ($ü \rightarrow ue$) and expand logistical shorthand ($LKW \rightarrow Truck$).

### Batch 2.1 Status: Complete (2026-04-13)
- All ERP encoding normalization and German string handling logic is implemented and validated in the Silver layer.
- `erp_maintenance_utf8` and `erp_maintenance_normalized` dbt models are operational and tested.
- See docs/phase-reports/phase-2/phase-2-silver-commands.md for full command log and outcomes.

### Batch 2.2: Numeric & Temporal Harmonization
* **Chunk 3: German Numeric Parser:** Transform German strings (`1.200,50`) into standard floats using `REPLACE` and `CAST` logic OR `regex`.
* **Chunk 4: The Surrogate Key Engine:** Use `dbt_utils.generate_surrogate_key` to create a `universal_asset_id` that links the NASA engines to the German maintenance events.

#### ✅ Batch 2.2 Status: Complete (2026-04-13)
- German numeric parser implemented: parses German-formatted numbers (e.g., "1.200,50") to floats in `erp_maintenance_numeric`.
- Surrogate key engine implemented: generates `universal_asset_id` in `erp_maintenance_surrogate` using `dbt_utils.generate_surrogate_key`.
- All models built and validated in DuckDB.
- See docs/phase-reports/phase-2/phase-2-silver-commands.md for full command log and outcomes.

### Batch 2.3: Integrity & Logic Contracts

### Objective
Implement data integrity and logic contracts at the Silver boundary using Great Expectations (GE) to ensure:
- All "quality" scores are between 0 and 1 (inclusive)
- All "sensor_timestamp" values are strictly increasing per unit (engine)

### Key Steps
- Created a new dbt Silver model `nasa_silver` for NASA sensor data, exposing:
  - `quality`: Min-max normalized sensor value (sensor 6) per unit, always between 0 and 1
  - `sensor_timestamp`: Uses the `cycle` column, strictly increasing per unit
- Ensured the model sorts and deduplicates by `unit_number` and `cycle` for monotonicity
- Implemented a Great Expectations suite in Python to validate:
  - All `quality` values are in [0, 1]
  - All `sensor_timestamp` values are strictly increasing per unit
- Ran the GE suite and confirmed both expectations pass on the Silver table

### Architectural/Naming Choices
- **Physical Table Naming:** NASA raw data is ingested as `bronze_nasa_train_physical` to avoid dbt recursion issues. The dbt model `bronze_nasa_train` is a view on this physical table, enabling clean separation between ingestion and modeling layers.
- **Silver Model Naming:** The Silver model is named `nasa_silver` to clearly indicate its layer and source. This avoids confusion with raw/bronze tables and supports modular pipeline design.
- **Quality Definition:** "quality" is defined as a min-max normalized value of sensor 6 (column 5) per unit, ensuring it is always in [0, 1] and suitable for downstream OEE logic.
- **Timestamp Definition:** "sensor_timestamp" is set to the `cycle` column, which is naturally strictly increasing per unit. Sorting and deduplication are enforced in the model to guarantee monotonicity.
- **Validation Approach:** Great Expectations is used outside dbt for flexible, script-driven validation, as dbt-native tests are less expressive for these contracts.

### Commands Executed
- `python3 scripts/ingest_nasa_to_duckdb.py`  
  *Ingest NASA sensor data as bronze_nasa_train_physical*
- `dbt run --select bronze.bronze_nasa_train --project-dir dbt --profiles-dir dbt`  
  *Register bronze_nasa_train as a dbt view on the physical table*
- `dbt run --select silver.nasa_silver --project-dir dbt --profiles-dir dbt`  
  *Build Silver layer model with contract-compliant fields*
- `python3 great_expectations/run_silver_suite.py`  
  *Run GE suite to validate quality and timestamp contracts*

### Outcome
- `nasa_silver` table created and validated in DuckDB.
- All "quality" values are between 0 and 1; all "sensor_timestamp" values are strictly increasing per unit.
- Batch 2.3 requirements are fully met and contract-compliant.

---

# Phase 3: Analytics Engineering & OEE Logic (Gold Layer)
**Goal:** Implement the complex SQL math required for factory efficiency metrics. Architect the core OEE metrics and maintain historical asset state.

### Batch 3.1: The OEE Calculator
* **Chunk 1: Availability & Performance Models:** Calculate the core components of Overall Equipment Effectiveness:
	$$Availability = \frac{\text{Operating Time}}{\text{Planned Production Time}}$$
	$$Performance = \frac{\text{Actual Throughput}}{\text{Target Throughput}}$$
* **Chunk 2: Quality & OEE Final:** Aggregate the metrics into a final OEE score:
	$$OEE = Availability \times Performance \times Quality$$ at the asset and factory levels.

### Batch 3.1 Status: Complete (2026-04-13)
- Gold layer models `oee_availability_performance` and `oee_final` implemented in `dbt/models/gold/`.
- Models calculate Availability, Performance, and aggregate OEE at the asset level using Silver layer outputs.
- All models built and validated in DuckDB. Sample output:

| unit_number | availability | performance | quality   | oee      |
|-------------|--------------|-------------|-----------|----------|
| 1           | 1.0          | 1.0         | 0.060269  | 0.060269 |
| 2           | 1.0          | 1.0         | 1.000000  | 1.000000 |
| ...         | ...          | ...         | ...       | ...      |

- See `docs/phase-reports/phase-3/phase-3-gold-commands.md` for full command log and outcomes.

### Batch 3.2: Asset History (SCD Type 2)
* **Chunk 3: dbt Snapshots:** Initialize `dbt snapshots` on the equipment status table. This preserves the history of machine "States" (e.g., *Operational*, *Degraded*, *Maintenance*).
* **Chunk 4: Late-Arriving Data Buffer:** Implement a windowed dbt incremental model to capture sensor heartbeats that arrive out of sequence.

### Batch 3.2 Status: Complete (2026-04-13)
- SCD Type 2 snapshot `erp_equipment_status_snapshot` implemented in `dbt/snapshots/` and executed, preserving equipment status history.
- Incremental model `nasa_late_arrival_buffer` implemented in `dbt/models/gold/` and executed, ready to flag late-arriving NASA sensor heartbeats.
- All models built and validated in DuckDB. No late arrivals detected in current data.
- See `docs/phase-reports/phase-3/phase-3-gold-commands.md` for full command log and outcomes.

### Batch 3.3: Integrity & Logic Contracts

### Objective
Implement data integrity and logic contracts at the Gold boundary using Great Expectations (GE) to ensure:
- All "quality" scores are between 0 and 1 (inclusive)
- All "sensor_timestamp" values are strictly increasing per unit (engine)

### Key Steps
- Created a new dbt Gold model `nasa_gold` for NASA sensor data, exposing:
  - `quality`: Min-max normalized sensor value (sensor 6) per unit, always between 0 and 1
  - `sensor_timestamp`: Uses the `cycle` column, strictly increasing per unit
- Ensured the model sorts and deduplicates by `unit_number` and `cycle` for monotonicity
- Implemented a Great Expectations suite in Python to validate:
  - All `quality` values are in [0, 1]
  - All `sensor_timestamp` values are strictly increasing per unit
- Ran the GE suite and confirmed both expectations pass on the Gold table

### Batch 3.3 Status: Complete (2026-04-13)
- Gold layer model `nasa_gold` implemented in `dbt/models/gold/`.
- Model exposes min-max normalized `quality` and strictly increasing `sensor_timestamp` per unit, using the same logic as Silver.
- Great Expectations suite implemented and run in `great_expectations/run_gold_suite.py`.
- All integrity and logic contracts validated: all `quality` in [0, 1], all `sensor_timestamp` strictly increasing per unit.
- See `docs/phase-reports/phase-3/phase-3-gold-batch-3-3.md` for full command log and outcomes.

### Architectural/Naming Choices
- **Physical Table Naming:** NASA raw data is ingested as `bronze_nasa_train_physical` to avoid dbt recursion issues. The dbt model `bronze_nasa_train` is a view on this physical table, enabling clean separation between ingestion and modeling layers.
- **Gold Model Naming:** The Gold model is named `nasa_gold` to clearly indicate its layer and source. This avoids confusion with raw/bronze tables and supports modular pipeline design.
- **Quality Definition:** "quality" is defined as a min-max normalized value of sensor 6 (column 5) per unit, ensuring it is always in [0, 1] and suitable for downstream OEE logic.
- **Timestamp Definition:** "sensor_timestamp" is set to the `cycle` column, which is naturally strictly increasing per unit. Sorting and deduplication are enforced in the model to guarantee monotonicity.
- **Validation Approach:** Great Expectations is used outside dbt for flexible, script-driven validation, as dbt-native tests are less expressive for these contracts.

### Commands Executed
- `python3 scripts/ingest_nasa_to_duckdb.py`  
  *Ingest NASA sensor data as bronze_nasa_train_physical*
- `dbt run --select bronze.bronze_nasa_train --project-dir dbt --profiles-dir dbt`  
  *Register bronze_nasa_train as a dbt view on the physical table*
- `dbt run --select gold.nasa_gold --project-dir dbt --profiles-dir dbt`  
  *Build Gold layer model with contract-compliant fields*
- `python3 great_expectations/run_gold_suite.py`  
  *Run GE suite to validate quality and timestamp contracts*

### Outcome
- `nasa_gold` table created and validated in DuckDB.
- All "quality" values are between 0 and 1; all "sensor_timestamp" values are strictly increasing per unit.
- Batch 3.3 requirements are fully met and contract-compliant.

---

# Phase 4: Predictive Intelligence & ML Tournament
**Goal:** Deploy Scikit-learn within dbt to predict machine failure and remaining life. Deploy in-warehouse Machine Learning to predict Remaining Useful Life (RUL).

### Batch 4.1: Prognostics (RUL Prediction)
* **Chunk 1: Feature Engineering:** Calculate sensor slopes, rolling standard deviations, and lag features to detect degradation patterns. In addition, use dbt-SQL to create rolling averages and variance features for the NASA vibration sensors.
* **Chunk 2: RUL Regressor:** Implement a **dbt-Python model** to run **Scikit-learn** inside DuckDB. Train a **Random Forest Regressor** to predict **Remaining Useful Life (RUL)**:
	$$RUL_{target} = Cycle_{max} - Cycle_{current}$$

### Batch 4.2: Benchmarking & Segmentation

* **Chunk 3: The Algorithm Tournament:**
  - Benchmarked Random Forest, Linear Regression, and XGBoost for RUL prediction.
  - Applied advanced enhancements: hyperparameter tuning, scaling, regularization, cross-validation, and SHAP explainability (where appropriate).
  - RMSE results are stored in the `model_performance` table; the best model is flagged.
  - Enhanced models outperformed initial baselines in both accuracy and robustness.

* **Chunk 4: Anomaly Clustering:**
  - KMeans clustering (with feature scaling) segments sensor anomalies into failure modes (e.g., Thermal Fatigue, High Vibration).
  - Assets are clustered into "Health Zones" (Green/Yellow/Red) based on RUL and sensor features.
  - Cluster statistics (mean/std of RUL and features) are stored in `kmeans_cluster_diagnostics` for interpretability.

**Summary:**
All enhancements were justified for this industrial dataset. Tuning, scaling, diagnostics, and explainability improved both accuracy and trustworthiness. Not all enhancements are equally critical for every algorithm, but all contribute to a robust, production-ready solution. See `docs/phase-reports/phase-4/phase-4-ml-tournament-report.md` for full results and analysis.

---

# Phase 5: Generative AI & Executive Storytelling
**Goal:** Humanize the technical output via a "Maintenance Copilot." That is, Bridge the gap between data and the end-user.

### Batch 5.1: The Semantic Layer
* **Chunk 1: Global Health Index:** Define the **"Factory Health Index"** ($FHI$) as a unified metric across the organization:
	$$FHI = w_1(OEE) + w_2(RUL_{normalized})$$

### Batch 5.2: LLM Copilot Implementation
* **Chunk 2: Streamlit Interface:** Build a Python app in the Codespace that queries your Gold Marts.
* **Chunk 3: LLM Context Synthesis/Automated Root-Cause:** Feed the dbt metadata and current sensor anomalies to the LLM. **Contextual Prompting:** Build a **Streamlit** app that pulls the latest OEE scores, ML predictions, and German maintenance logs.
	* *Result:* An engineer asks: "Why is Line 4 red?" The LLM explains: "Motor A shows a 20% vibration increase (Pattern: Bearing Wear). RUL is predicted at 12 cycles."
	* *Result:* User asks "Why is Line 4 failing?" LLM responds: "RUL is <10 cycles. German logs show a 'Lagerdefekt' (bearing defect) was noted in München 2 weeks ago, and vibration has since spiked by 25%."
* **Chunk 4: Metabase Dashboards: Connect Metabase to DuckDB for high-level OEE trend visualization.

---

# Phase 6: Governance, CI/CD & Observability
**Goal:** Ensure the system is self-healing, accurate, and ready for production.

### Batch 6.1: Quality Gates & Monitoring
* **Chunk 1: Great Expectations (GE) Suites:** Validate that OEE percentages stay between $0$ and $1$. Verify that NASA sensor data contains no "Ghost" values.
* **Chunk 2: Observability - Monte Carlo Lineage:** Deploy Monte Carlo to monitor DuckDB tables. Map the end-to-end lineage. Trigger an alert if the **IoT Heartbeat** from the factory stalls for $>15$ minutes.

### Batch 6.2: CI/CD & Final Delivery
* **Chunk 3: GitHub Actions "Slim CI":** Configure a workflow to run `dbt test` on modified models only during a Pull Request. Configure an automated pipeline that runs dbt test on every Pull Request, ensuring the "German Cleaning" logic is never broken by new code.
* **Chunk 4: The MSc Runbook:** Generate the final documentation including the Project Walkthrough, Business Blueprint, and Command Logs.

---

## 2026-04-12: Batch Commit Correction & Traceability Enhancement

**Summary:**
To restore traceability, a mistaken large batch commit was replaced with a series of smaller, logical batch commits (data, architecture, business, command, etc.), each with a clear message. The improved history was force-pushed to the remote repository.

**Rationale:**
- Ensures each change is reviewable and auditable.
- Aligns with best practices for collaborative and thesis-level projects.

**Lessons Learned:**
- Commit in logical batches, not all at once.
- Document all corrective actions and commands.
- Keep command and runbook files up to date for full transparency.

---

### Why this is "Thesis-Level" Prowess:
By the end of this plan, you will have built a **fully functional, predictive industrial system** on a local DuckDB engine. You will have successfully navigated:
1. Complex Encodings: Solving for the "German Constraint."
2. Advanced Modeling: Running RUL and Anomaly clustering in-warehouse.
3. Governance: Using Monte Carlo and GE to guarantee reliability.
4. Modern AI: Implementing a "copilot" that actually understands the manufacturing context.

### How this project prepares you for the Job Market
By completing this specific plan, you are demonstrating **Product-Minded Engineering**. In an interview with a company like **G2B/SaaS**, you can prove:
1.  **Technical Depth:** You can build ML models *inside* a data warehouse.
2.  **Market Awareness:** You understand how to handle legacy German data (Encoding/Umlauts).
3.  **Modern Stack Mastery:** You can orchestrate a "headless" system using GitHub Secrets and Airflow.
4.  **Strategic Communication:** You can turn "sensor noise" into a "Maintenance Copilot" for non-technical stakeholders.

# Why this Plan Delivers Business and Academic Value
By following this plan, you will deliver a fully functional, explainable, and governed predictive maintenance system. You will demonstrate:
- Technical depth (ML in-warehouse, encoding/normalization, CI/CD)
- Business impact (downtime reduction, OEE improvement, actionable insights)
- Modern engineering practices (reproducibility, auditability, stakeholder enablement)

### 2026-04-13: Phase 3 Data Quality & Engineering Improvements

**Summary:**
To align with modern industry standards and ensure robust analytics, the following improvements were made to the Silver and Gold NASA sensor data layers:

#### 1. dbt-native Data Quality Tests
- Added dbt-native tests for:
  - Not null constraints on `unit_number`, `sensor_timestamp`, and `quality`.
  - Multi-column uniqueness on `(unit_number, sensor_timestamp)` using `dbt_utils.unique_combination_of_columns`.
  - Value range check for `quality` using `dbt_utils.expression_is_true` to ensure all values are in [0, 1].
- These tests now run with `dbt test` and all pass, providing fast, CI-friendly validation.

#### 2. SQL Optimization & Explicit Column Selection
- Refactored both `nasa_silver.sql` and `nasa_gold.sql` to:
  - Select only required columns (no `select *`).
  - Use explicit column names for clarity and performance.
- This reduces unnecessary data movement and improves maintainability.

#### 3. Macro Reuse for Min-Max Normalization
- Created a macro `min_max_normalize` in `dbt/macros/min_max_normalize.sql` to encapsulate the normalization logic.
- Both Silver and Gold models now use this macro for the `quality` calculation, ensuring consistency and easier future updates.

**Outcome:**
- All dbt-native tests pass for both layers.
- Data models are more efficient, maintainable, and aligned with best practices.
- The pipeline is now robust, testable, and ready for further enhancements or productionization.