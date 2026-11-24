---
paths:
  - "migrations/**"
  - "docs/features/*/migrations/**"
---

# Migration rules (SQLite)

<!-- Bootstrapped by data-model-builder. Edit freely; an existing file wins over the skill. -->

## Filenames

- `NNNN_<verb>_<entity>.up.sql` + matching `.down.sql`, four digits, applied in name order by
  `src/evidence_meter/platform/migrate.py` (`make migrate`; revert the newest with
  `uv run python -m evidence_meter.platform.migrate --revert`).
- A feature's migrations are designed in `docs/features/<slug>/migrations/` and moved to `migrations/`
  when they are proved with apply, no-op and revert.

## Hard rules (DB as dumb storage)

- No `CHECK` constraints on business invariants, except one recorded in an Accepted ADR and commented in
  the SQL with the ADR number.
- No `CREATE TRIGGER`, no views, no stored logic.
- No `DEFAULT` at all, timestamps included.
- Business logic lives in app code.

## Required constraints

- Every `REFERENCES` column has an index whose first column is that column.
- Every `.up.sql` has a `.down.sql` that fully reverses it; drop children before parents.
- `CREATE TABLE` / `CREATE INDEX` use `IF NOT EXISTS`; `DROP` uses `IF EXISTS`. `ALTER TABLE ADD COLUMN`
  has no `IF NOT EXISTS` in SQLite; the runner's per-file transaction and `schema_migrations` row are
  the guard.
- No `BEGIN` / `COMMIT` in a file: the runner wraps each file and its `schema_migrations` row in one
  transaction.
- Foreign keys are declared but SQLite enforces them only with `PRAGMA foreign_keys = ON` on the
  connection; `platform/db.py` turns it on (the runner does not, so a table rebuild can drop a parent).

## Defaults

- Tables are `STRICT` (SQLite 3.37+): declared types are enforced.
- Types: `INTEGER`, `REAL`, `TEXT` only. No `VARCHAR(N)`: SQLite ignores the bound, so bounds live in
  the app's validation and in `data-model.md`.
- PK: `id INTEGER PRIMARY KEY` (rowid alias). Identity is the natural `UNIQUE` key the SAD names.
- Timestamps: `TEXT NOT NULL`, ISO 8601 UTC with `Z`, set by the app. One creation timestamp per table,
  named for its event (`imported_at`, `computed_at`). No `updated_at`: rows are immutable.
- Hashes: `TEXT`, lowercase hex SHA-256 (64 characters).
- Hard delete only; no `deleted_at`.
- Names: plural `snake_case` tables prefixed with the owning context (`collection_`, `computation_`); a
  context writes only its own prefix. No foreign key crosses a context: a reference across contexts is a
  hash column.
- JSON: `TEXT` holding a canonical JSON form only when that form is what gets hashed; structured fields
  that a query filters on are columns.

## Changing an existing table

- New NOT NULL column, rename or drop: three migrations, expand (add nullable, the app writes both) →
  backfill (an `UPDATE`, with a companion `backfill-<column>.md`) → contract.
- SQLite cannot `ALTER COLUMN`: a contract that adds `NOT NULL` or changes a type rebuilds the table
  (create `<table>_new`, copy, drop, rename, recreate its indexes) with `foreign_keys` off, as SQLite's
  documented 12-step procedure says.
- New index on an existing table: plain `CREATE INDEX IF NOT EXISTS`.

## Seeds

- Lookup data: a separate migration with `INSERT ... ON CONFLICT DO NOTHING`.
- Test fixtures are never in `migrations/`: tests build a temp SQLite file with the runner and insert
  synthetic rows (`team-alpha`, `PRJ-DEMO-1`).
- No real-looking names, teams, project keys or tracker states anywhere (AGENTS.md).

## Out of scope

- Replicas, sharding, partitioning, materialized views.
