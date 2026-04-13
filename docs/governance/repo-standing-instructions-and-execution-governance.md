## Purpose
This document defines the governance, quality, and documentation standards for the Predictive OEE PHM Engine. It ensures phase-by-phase, batch-driven delivery is reproducible, auditable, and thesis-ready—tailored for a local-first, open-source stack (Codespaces, DuckDB, dbt, Airbyte, Streamlit). All orchestration is now native (Makefile and shell scripts); Docker and Git LFS are no longer used.

4. **Do not use Docker or Git LFS for orchestration or data management. All services and data are managed natively.**


# Repo Standing Instructions and Execution Governance: Predictive OEE PHM Engine

## Standing Instructions (Critical Enforcement)

1. **Do NOT commit or push any files or folders from `legacy-files/` under any circumstances.**
2. **At the successful completion of each batch in every phase, always commit and push all relevant changes before proceeding.**
3. **After each batch, update all necessary documentation files (README, runbook, command logs, phase reports, etc.) to reflect the work completed and lessons learned.**

These instructions are mandatory and take precedence over all other workflow steps. Violations must be documented in the incident log and corrected immediately.

## Purpose
This document defines the governance, quality, and documentation standards for the Predictive OEE PHM Engine. It ensures phase-by-phase, batch-driven delivery is reproducible, auditable, and thesis-ready—tailored for a local-first, open-source stack (Codespaces, DuckDB, dbt, Airbyte, Streamlit).

## 1. Batch Execution Protocol
Every batch must:
1. **Scope Announcement:** Clearly define batch and chunk boundaries before implementation (e.g., "Batch 1.1, Chunk 3: Sensor ingestion script").
2. **Atomic Commits:** Use `type(scope): summary` commit messages (e.g., `feat(ingest): add NASA loader`).
3. **Environment Sync:** Verify Codespace, dbt, DuckDB, Airbyte, and Streamlit versions before execution.
4. **Validation Gate:** Include successful quality checks (`dbt test`, Great Expectations, unit tests) in the batch summary.
5. **Documentation Maintenance:** Update all relevant .md files (specs, phase reports, runbooks) in the same change set.
6. **Rollback Readiness:** For schema/model changes, include a short rollback note.

## 2. Batch Documentation Report Template
For each batch, use the following template in `docs/phase-reports/`:

### Batch Metadata
- Batch ID (e.g., OEE-P2-B1.2)
- Phase (Ingestion, Transformation, Analytics, Copilot/UI, Governance)
- Status (Draft, Completed, Verified)
- Environment profile and runtime target

### What Was Built
- Files created or modified
- Data model, pipeline, or infrastructure changes
- Connectivity and runtime check result

### Tool and Methodology Justifications
- Methodology rationale (e.g., why dbt, why K-means)
- German constraint handling rationale (encoding, decimal, character normalization)
- Trade-offs and alternatives considered

### Issues & Resolutions
- Incident
- Root cause
- Resolution

### Acceptance Criteria Met
- [ ] Encoding and normalization tests pass
- [ ] Ingestion detects newly landed files
- [ ] Schema and quality checks pass
- [ ] Freshness SLA and incident thresholds validated

## 3. Command Log Policy
Maintain and update command logs under `docs/command/`. This is critical for the "Runbook" deliverable.

Command logging is mandatory across the full project lifecycle:
- No command category is excluded.
- Every command run for implementation, validation, deployment, or troubleshooting must be documented.
- Use `docs/command/README.md` as the command register and append entries in the appropriate category file.

Minimum required command log files:
- `duckdb-commands.md` (local execution track)
- `dbt-commands.md`
- `bash-shell-commands.md`
- `make-commands.md`
- `git-commands.md`
- `github-actions-commands.md`
- `python-commands.md`
- `airflow-commands.md`
- `airbyte-commands.md`
- `docker-commands.md`
- `lint-commands.md`

## 4. Deliverables Index Policy
The `README.md` must serve as the **Thesis Portfolio Map**.

Required document set:
- **Thesis Defense Brief**
- **Technical Project Presentation** (architecture diagrams, Medallion flow)
- **Non-Technical Business Blueprint** (value prop, ROI, business questions)
- **Developer Inner Loop Walkthrough** (Codespace, dbt, Airbyte, DuckDB)
- **German Data Normalization Appendix**
- **Project Runbook** (step-by-step reproduction guide)
- **SLA & Observability Report** (Monte Carlo incident logs)
- **Standard MSc thesis report** (5 chapters: Introduction, Literature Review, Methodology, Implementation & Evaluation, Results & Recommendations)

## 5. Issues and Incident Documentation (The "Incident Post-Mortem")
Maintain per-phase issue logs in `docs/incidents/`:
- **Symptom:** What the developer saw
- **Cause:** (e.g., data error, pipeline failure, environment mismatch)
- **Solution Implementation:** The specific CLI command or code fix
- **How to avoid recurrence**
- **Mastery Lesson:** How this prepares you for a real-world analytics engineering role

## 6. Data Governance & LFS Policy
- **Git LFS:** Use for large CSVs if needed (e.g., Kaggle datasets)
- **Data Privacy:** Any PII must be masked or hashed in the Bronze-to-Silver transition
- **Metadata Discipline:** All curated models must include descriptions, owners, and quality expectations

## 7. Phase Checkpoint & Promotion Policy
Before promoting a phase:
1. **SLA Validation:** Confirm required freshness window (e.g., Gold-layer health metrics updated every 15 minutes)
2. **Lineage Verification:** Confirm source-to-gold traceability (Monte Carlo or equivalent)
3. **German Consistency Checks:** Verify character and numeric normalization
4. **Handover Review:** Confirm another engineer can reproduce the phase

## 8. Developer Inner Loop Enforcement
- Author code locally in Codespaces with version control
- Execute through scripted workflows and tracked commands
- Keep Git as the single source of truth; avoid unmanaged edits

---

### Implementation Note
This document is the "Constitution" of the Predictive OEE PHM Engine repository. Adhering to it demonstrates both technical capability and production-grade engineering governance.