---
status: Accepted
date: 2026-11-22
---

# ADR 0003: Persistence — SQLite with plain SQL migrations and a standard-library runner

## Context and problem statement

The tool keeps snapshots, measurements, verdicts and pages for one organisation on one machine.

## Decision drivers

- No server to run for development or tests.
- Migrations readable as SQL, in the same up/down pairs `generate-data-model` produces.
- No dependency where the standard library is enough.

## Considered options

1. SQLite via `sqlite3`, `migrations/NNNN_<name>.up.sql` and `.down.sql`, runner in `platform/migrate.py`.
2. SQLite with Alembic (and SQLAlchemy).
3. PostgreSQL in Docker.

## Decision outcome

Option 1. The runner applies pending `up` files in order inside a transaction each, records them in
`schema_migrations`, and reverts the last one with its `down` file. Each context owns its tables. IDs and
table design are left to the data model (S7).

### Consequences

- Good: integration tests use a temp SQLite file; no container.
- Bad: the runner is our code to maintain; switch to a tool if migrations need branching or data fixes.
