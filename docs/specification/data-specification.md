# Data Specification Template


## 1. Data Sources
- NASA Turbofan sensor data and simulated German ERP logs are ingested directly into the workspace (no LFS or external large file management required).
- Data provenance and versioning are managed via Git and batch execution logs.

## 2. Data Schemas
- Schema definitions for each source
- Data dictionaries (field names, types, descriptions)

## 3. Data Quality Rules
- Validation rules (dbt, Great Expectations)
- Handling of missing, anomalous, or duplicate data

## 4. Data Transformation
- Mapping and normalization logic
- Surrogate key generation

## 5. Data Lineage
- Data flow from ingestion to gold layer
- Lineage diagrams (if available)

## 6. Data Security & Privacy
- Sensitive fields and masking requirements

## 7. Appendices
- Example data, reference tables, and glossary
