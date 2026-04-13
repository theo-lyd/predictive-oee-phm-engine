This implementation plan is structured to follow the **Developer Inner Loop** philosophy, ensuring that your **GitHub Codespace** acts as the command center while your data warehouse (DuckDB or Snowflake) handles the heavy lifting. Each phase is broken down into **Batches** (scope) and **Chunks** (atomic tasks) to ensure a systematic, thesis-level delivery.

---

# Phase 1: Foundation & Resilient Ingestion
**Goal:** Establish the infrastructure and automate the retrieval of multi-modal data.


### Batch 1.1: Environment & Secret Management
* **Chunk 1: Codespace Orchestration:** Configure `.devcontainer` to install `dbt-core`, `airflow`, `kaggle CLI`, DuckDB CLI, and `duckdb`.
* **Chunk 2: Secure Credentials:** Inject `KAGGLE_USERNAME` and `KAGGLE_KEY` into GitHub Secrets. Map them to the Codespace environment.
* **Chunk 3: Orchestration Setup:** Use Makefile and shell scripts to launch Airflow, dbt, and Postgres as native services (no Docker required). Define the SCRIPTS_DIR for Python ingestion and DBT_DIR for transformations.
* **Chunk 4: DuckDB Persistence:** Initialize factory_analytics.db. Configure dbt profiles to point to this local file, ensuring it is mounted to a persistent volume.


### Batch 1.2: The "Dual Intake" Pipeline
* **Chunk 5: NASA IoT Ingestion:** Write a Bash script to pull the **Turbofan Failure Data** via Kaggle CLI. Unzip into `data/raw/sensors/`. Implement a bash script triggered by Airflow that uses the Kaggle API (authenticated via GitHub Secrets) to pull the NASA Turbofan dataset into data/raw/sensors/ (no LFS required).
* **Chunk 6: German ERP Simulation:** Execute `generate_german_erp.py` to create the legacy maintenance logs. 
	* *Requirement:* Ensure the file is encoded in **ISO-8859-1** with German numeric formats (e.g., `1.500,00`). Export files in ISO-8859-1 encoding. Use German status strings (Instandhaltung erforderlich) and factory locations with Umlaute (München, Göttingen).
* **Chunk 7: Airbyte/Postgres Setup:** Configure Airbyte to sync the simulated ERP data from a local Postgres instance into the Bronze layer. Use Airbyte (running natively) to ingest the simulated ERP Postgres tables and the CSV sensor files into the Bronze Schema of DuckDB.

---

# Phase 2: The "German" Data Refinery (Silver Layer)
**Goal:** Neutralize data "noise", harmonize disparate sources, and solve the German encoding/normalization challenges. 

### Batch 2.1: Encoding & String Normalization and Character Mapping
* **Chunk 1: The Encoding Shield:** Create a dbt macro to cast the raw ERP strings from `ISO-8859-1` to `UTF-8`. Encoding Shield: Develop dbt models that cast ISO-8859-1 raw strings into clean UTF-8
* **Chunk 2: Umlaut & Abbreviation Logic:** Write SQL regex patterns to replace Umlaute (e.g., `Lagerstörung` $\rightarrow$ `Lagerstoerung`) and expand shorthand (e.g., `Prüf.` $\rightarrow$ `Pruefung`). Create a dbt macro to map German characters ($ü \rightarrow ue$) and expand logistical shorthand ($LKW \rightarrow Truck$).

### Batch 2.2: Numeric & Temporal Harmonization
* **Chunk 3: German Numeric Parser:** Transform German strings (`1.200,50`) into standard floats using `REPLACE` and `CAST` logic OR `regex`.
* **Chunk 4: The Surrogate Key Engine:** Use `dbt_utils.generate_surrogate_key` to create a `universal_asset_id` that links the NASA engines to the German maintenance events.

### Batch 2.3: Integrity & Logic Contracts
* **Chunk 5: Great Expectations (GE) Suite: Define GE checkpoints at the Silver boundary to ensure "Quality" scores are between $0$ and $1$ and that sensor timestamps are strictly increasing.
---

# Phase 3: Analytics Engineering & OEE Logic (Gold Layer)
**Goal:** Implement the complex SQL math required for factory efficiency metrics. Architect the core OEE metrics and maintain historical asset state.

### Batch 3.1: The OEE Calculator
* **Chunk 1: Availability & Performance Models:** Calculate the core components of Overall Equipment Effectiveness:
	$$Availability = \frac{\text{Operating Time}}{\text{Planned Production Time}}$$
	$$Performance = \frac{\text{Actual Throughput}}{\text{Target Throughput}}$$
* **Chunk 2: Quality & OEE Final:** Aggregate the metrics into a final OEE score:
	$$OEE = Availability \times Performance \times Quality$$ at the asset and factory levels.

### Batch 3.2: Asset History (SCD Type 2)
* **Chunk 3: dbt Snapshots:** Initialize `dbt snapshots` on the equipment status table. This preserves the history of machine "States" (e.g., *Operational*, *Degraded*, *Maintenance*).
* **Chunk 4: Late-Arriving Data Buffer:** Implement a windowed dbt incremental model to capture sensor heartbeats that arrive out of sequence.

---

# Phase 4: Predictive Intelligence & ML Tournament
**Goal:** Deploy Scikit-learn within dbt to predict machine failure and remaining life. Deploy in-warehouse Machine Learning to predict Remaining Useful Life (RUL).

### Batch 4.1: Prognostics (RUL Prediction)
* **Chunk 1: Feature Engineering:** Calculate sensor slopes, rolling standard deviations, and lag features to detect degradation patterns. In addition, use dbt-SQL to create rolling averages and variance features for the NASA vibration sensors.
* **Chunk 2: RUL Regressor:** Implement a **dbt-Python model** to run **Scikit-learn** inside DuckDB. Train a **Random Forest Regressor** to predict **Remaining Useful Life (RUL)**:
	$$RUL_{target} = Cycle_{max} - Cycle_{current}$$

### Batch 4.2: Benchmarking & Segmentation
* **Chunk 3: The Algorithm Tournament:** Benchmark the Random Forest against a **Linear Regression** and **XGBoost**. Store RMSE (Root Mean Square Error) results in a `model_performance` table and compare RMSE (Root Mean Square Error) to determine the "Production Model."
* **Chunk 4: Anomaly Clustering:** Use **K-Means Clustering** to segment sensor anomalies into specific failure modes (e.g., *Thermal Fatigue* vs. *High Vibration*). Cluster machines into "Health Zones" (Green/Yellow/Red) based on the current probability of failure.

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