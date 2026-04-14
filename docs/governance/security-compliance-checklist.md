# Security & Compliance Checklist

- [x] All credentials (e.g., Kaggle, Metabase) are managed via GitHub Secrets or environment variables.
- [x] No hardcoded secrets in code or config files.
- [x] .gitignore covers .env, .venv, and sensitive data.
- [x] All CI/CD and monitoring actions are logged (see GitHub Actions logs and monitoring script logs).
- [x] Audit logs are retained in docs/command/ and GitHub Actions for compliance.

## How to Rotate Secrets
- Update GitHub Secrets in the repository settings.
- Re-run failed workflows after secret rotation.

## How to Audit Actions
- Review GitHub Actions logs for all workflow runs.
- Check docs/command/ for manual command logs.
- Monitoring script logs are written to stdout and can be redirected to a file if needed.
