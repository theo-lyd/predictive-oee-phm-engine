

# Project Details: Predictive OEE PHM Engine

## Executive Summary
This project delivers a production-grade, governed analytics and AI system for Industry 4.0 maintenance. It is designed to maximize production throughput, reduce unplanned downtime, and empower both technical and non-technical stakeholders with actionable insights. The approach integrates best-in-class data engineering, machine learning, and business process rigor.

## 1. Business Context & Objectives
Unplanned downtime is a major source of lost revenue and operational inefficiency. This project addresses the challenge by harmonizing high-frequency IoT sensor data with legacy ERP maintenance logs, enabling predictive and prescriptive maintenance. The goal is to move from reactive to proactive decision-making, with measurable business impact.

**Key Objectives:**
- Reduce unplanned downtime by >30% in year 1
- Improve OEE by >5% across all lines
- Increase accuracy of RUL predictions (target: RMSE < 10 cycles)
- Ensure full auditability and compliance with DACH-region standards

## 2. Technical Architecture & Stack
- **Environment:** GitHub Codespaces (Dockerized)
- **Ingestion:** Airbyte (ERP logs), Python/Airflow (IoT)
- **Storage/Compute:** DuckDB (local), Snowflake (cloud)
- **Transformation:** dbt (SQL/Python)
- **ML:** Scikit-learn (RUL, clustering, forecasting)
- **Observability:** Monte Carlo, Great Expectations
- **Orchestration:** Airflow
- **CI/CD:** GitHub Actions
- **Interface:** Streamlit (Copilot), Metabase (Dashboards)

## 3. Implementation Roadmap (Phased)
**Phase I: Ingestion & Foundation**
- Set up secure, reproducible ingestion for both NASA and simulated German ERP data
- Automate late-arrival handling and ensure full traceability

**Phase II: Data Refinery (Silver Layer)**
- Normalize encodings, harmonize business keys, and solve German data constraints
- Ensure data quality and schema consistency

**Phase III: Analytics Engineering (Gold Layer)**
- Calculate OEE, track asset health, and maintain SCD Type 2 history
- Build robust, tested marts for downstream analytics

**Phase IV: Predictive Intelligence**
- Engineer features, train and benchmark RUL models, segment anomalies
- Integrate explainable AI for actionable recommendations

**Phase V: Governance & Stakeholder Enablement**
- Deploy semantic layer, Copilot, and dashboards
- Enforce business rules, SLAs, and auditability

## 4. Business Rules & Compliance
1. Downtime >5 min = unplanned unless pre-registered
2. OEE <65% triggers triage
3. RUL/Quality guardrails: flag for calibration or incident if thresholds breached
4. All data must be audit-ready and encoding-compliant

## 5. Stakeholder Value & Success Metrics
- **COO/Leadership:** Real-time OEE, risk, and ROI dashboards
- **Maintenance:** Copilot for root-cause and prescriptive actions
- **Finance/Procurement:** RUL-driven inventory and spend optimization
- **Audit/Compliance:** Full traceability and incident evidence

**KPIs:**
- Unplanned downtime events (count, % reduction)
- OEE improvement (% increase)
- Maintenance cost per unit
- RUL prediction accuracy (RMSE)
- User adoption (% actions triggered by AI)

## 6. Change Management & Continuous Improvement
- All users receive training on Copilot and dashboards
- Feedback loops and quarterly model/business rule reviews
- Documentation and runbook updated per phase

## 7. Technical & Strategic Edge
This project demonstrates advanced data engineering, ML, and governance skills. It is designed to be both a production-ready solution and a distinguished academic thesis, with explicit benchmarking, explainability, and compliance features.

## 8. Implementation Details & Best Practices
- Use Kaggle API and GitHub Secrets for reproducible, secure data ingestion
- Simulate German ERP data with encoding and format challenges for realism
- Benchmark multiple ML models and document results
- Integrate semantic layer and explainable AI for business alignment

## 9. Summary
This project is a blueprint for governed, explainable, and business-aligned predictive maintenance in Industry 4.0. It bridges technical rigor and business value, ensuring measurable impact and stakeholder confidence.

---