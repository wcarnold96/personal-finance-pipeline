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

Plaid API (/transactions/sync, cursor-based)
↓
sync.py ──► S3 raw layer (JSONL, partitioned by sync_date)
↓
AWS Glue Data Catalog (partition projection)
↓
Amazon Athena
↓
dbt: stg_transactions → int_transactions_latest → fct_daily_cash_flow
↓
Dashboard


## Design notes

**Raw layer is immutable.** `sync.py` wraps each Plaid record with metadata (`item_id`,
`institution`, `change_type`, `sync_timestamp`) and writes it verbatim. No transformation
happens on ingest, so any modeling decision can be revisited without re-extracting.

**Incremental sync.** `/transactions/sync` returns `added`, `modified`, and `removed` since
the last cursor. The cursor is persisted per Item and written only after the S3 upload
succeeds — a failure between the two causes a re-fetch rather than data loss.

**Deduplication.** Because the raw layer accumulates every sync, a transaction can appear
multiple times as it is modified. `int_transactions_latest` keeps only the most recent
version of each `transaction_id` and excludes records that were later removed.

**Partition projection.** Athena computes partition values from the `sync_date` path pattern
rather than requiring `MSCK REPAIR TABLE` after each load, so new data is queryable the
moment it lands.

## Current state

- [x] Plaid Link integration — link token creation and public token exchange
- [x] Transaction sync via `/transactions/sync` with cursor-based incremental loads
- [x] S3 landing zone with date partitioning
- [x] Glue catalog and Athena external table with partition projection
- [x] dbt staging, intermediate, and mart models
- [x] dbt schema tests (uniqueness, null checks, accepted values) and a singular test
- [ ] Parquet conversion for query cost optimization
- [ ] Dashboard
- [ ] GitHub Actions CI running `dbt build`
- [ ] Terraform infrastructure
- [ ] Scheduled Lambda ingestion with tokens in SSM Parameter Store

## Known limitations

- Runs against Plaid Sandbox. Sandbox does not simulate pending transactions settling over
  time, so the `modified` and `removed` code paths are reasoned about but not observed
  against real settlement behaviour.
- Transfers between a user's own accounts are not yet excluded from cash flow, which
  inflates both inflow and outflow.
- `projection.sync_date.range` starts at a hardcoded date; it must be on or before the
  first sync.

## Repository layout

app.py one-time local Flask app for obtaining Plaid access tokens
plaid_client.py shared Plaid API client construction
sync.py pulls transactions and writes partitioned JSONL to S3
sql/transactions_raw.sql Athena DDL for the raw external table
finance_pipeline/ dbt project
models/staging/ flattening and type casting
models/intermediate/ deduplication to latest version per transaction
models/marts/ daily cash flow fact


## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in Plaid Sandbox credentials and your S3 bucket name.

Obtain access tokens (once per institution):

```bash
python app.py
```

Visit `localhost:5000` and complete the Plaid Link flow. Sandbox credentials are
`user_good` / `pass_good`. Tokens are written to a gitignored `tokens.json`.

Then sync and build:

```bash
python sync.py
cd finance_pipeline && dbt build
```

dbt connection settings live in `~/.dbt/profiles.yml` and are not committed.

## Notes

`app.py` is a one-time local utility, not a deployed service. The production pipeline runs
as a scheduled Lambda with no web server.
