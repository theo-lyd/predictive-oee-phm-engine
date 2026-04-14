# Master Backlog: Predictive OEE PHM Engine

| ID  | Epic/Story                                      | Description                                                                 | Effort (Points) | Role Owner(s)           | Sprint | Milestone                                   |
|-----|--------------------------------------------------|-----------------------------------------------------------------------------|-----------------|-------------------------|--------|----------------------------------------------|
| 1   | Data Ingestion                                  | Ingest NASA turbofan and synthetic ERP data (no LFS; native scripts)        | 8               | Data Engineer           | 1      | Raw data available in Bronze layer           |
| 2   | Encoding & Normalization                        | Normalize encodings, decimals, and characters                               | 5               | Data Engineer           | 1      | Clean, standardized raw data                 |
| 3   | Data Provenance & Versioning                    | Implement data versioning and provenance tracking                           | 3               | Data Engineer           | 1      | Ingestion logs and versioned datasets        |
| 4   | Silver Layer Transformation                     | Standardize schema, business keys, and surrogate keys                       | 8               | Analytics Engineer      | 2      | Silver-layer analytics-ready tables          |
| 5   | Data Quality Tests                              | Implement dbt and Great Expectations tests                                  | 5               | Analytics Engineer      | 2      | All quality tests passing                    |
| 6   | Gold Layer OEE & FHI Metrics                    | Calculate OEE and Factory Health Index (FHI)                                | 8               | Analytics Engineer      | 3      | Gold-layer marts with OEE/FHI                |
| 7   | RUL Target Calculation                          | Implement RUL calculation logic                                             | 5               | ML Engineer             | 3      | RUL features in gold layer                   |
| 8   | Baseline & Enhanced ML Models                   | Train, tune, and validate Linear Regression, Random Forest, XGBoost models  | 8               | ML Engineer             | 4      | Model benchmarks and enhancements            |
| 9   | Model Tournament & Selection                    | Benchmark all models, store RMSEs, select best production model             | 5               | ML Engineer             | 4      | Tournament results, best model flagged       |
| 10  | Segmentation & Clustering                       | Implement K-means clustering with scaling and diagnostics for degradation patterns | 5          | ML Engineer             | 4      | Asset clusters, health zones, diagnostics    |
| 11  | Model Evaluation & Explainability               | RMSE, MAE, diagnostics, and explainability artifacts (SHAP, feature importances) | 5         | ML Engineer             | 4      | Model evaluation report, phase 4 analysis    |
| 12  | Streamlit Maintenance Copilot                   | Build user-facing copilot for root-cause narration                          | 8               | BI Analyst, Analytics Engineer | 5  | Copilot UI deployed                          |
| 13  | Dashboard & Stakeholder Outputs                 | Develop dashboard-ready marts and visualizations                            | 5               | BI Analyst              | 5      | Dashboard available to stakeholders          |
| 14  | Observability & Alerting                        | Implement freshness/anomaly checks and alerting hooks                       | 5               | Analytics Engineer      | 5      | Alerts and observability in place            |
| 15  | Governance & Audit Trail                        | Document quality gates, SLAs, and audit trails                              | 5               | Analytics Engineer      | 6      | Governance documentation complete            |
| 16  | Runbook & Execution Evidence                    | Prepare runbook and execution evidence for reproducibility (native orchestration, no Docker/LFS) | 3               | Data Engineer           | 6      | Runbook and evidence delivered               |
| 17  | Phase Reports & Documentation                   | Complete phase reports and thesis-ready documentation                       | 5               | All                     | 6      | All documentation finalized                  |

## Sprint Milestones

- **Sprint 1:** Data ingestion, normalization, and provenance complete; raw data available
- **Sprint 2:** Silver-layer transformation and data quality tests complete
- **Sprint 3:** Gold-layer OEE/FHI and RUL features available
- **Sprint 4:** ML models trained, evaluated, and segmented
- **Sprint 5:** Copilot UI, dashboard, and observability delivered
- **Sprint 6:** Governance, runbook, and documentation finalized

---

- Effort points are relative (1 = trivial, 8 = major)
- Role ownership can be shared or rotated as needed
- Backlog is execution-ready and can be imported into JIRA or other tools
