# personal-finance-pipeline

End-to-end ELT pipeline for personal finance data: Plaid API → S3 → Athena → dbt → dashboard,
provisioned with Terraform and automated via GitHub Actions.

**Status:** In progress. Plaid ingestion working against Sandbox; S3 landing and
transformation layer not yet built.

## Motivation

Personal finance data is scattered across banks, credit cards, and brokerages, each with its
own export format. This project consolidates it into a single queryable data lake and models
it into marts for tracking net worth, cash flow, and savings rate over time.

## Architecture

Plaid API → Lambda (scheduled) → S3 (raw JSON)
↓
Parquet conversion
↓
AWS Glue Catalog → Amazon Athena
↓
dbt (staging → marts)
↓
Dashboard


Infrastructure defined in Terraform. CI/CD via GitHub Actions.

## Current state

- [x] Plaid Link integration — link token creation and public token exchange
- [x] Transaction sync via `/transactions/sync` with cursor-based incremental loads
- [x] S3 landing zone with date partitioning
- [ ] Parquet conversion
- [ ] Glue catalog and Athena tables
- [ ] dbt staging models and marts
- [ ] Terraform infrastructure
- [ ] Scheduled Lambda ingestion
- [ ] Dashboard

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` with Plaid Sandbox credentials:

PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_sandbox_secret


Run the token acquisition app:

NOTE: Much of this can be found in the Plaid documentation. For example https://plaid.com/docs/assets/add-to-app/ will walk you through linking a bank and the flow of access tokens

```bash
python app.py
```

Visit `localhost:5000` and complete the Plaid Link flow. Sandbox credentials are
`user_good` / `pass_good`. The resulting access token is used by the ingestion
job and is never committed.

## Notes

`app.py` is a one-time local utility for obtaining Plaid access tokens, not a deployed
service. The production pipeline runs as a scheduled Lambda with no web server.

