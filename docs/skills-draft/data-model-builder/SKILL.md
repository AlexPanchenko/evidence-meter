---
name: data-model-builder
description: Turn a feature's SAD (with §6 sequence flows and a coverage table) into data-model.md plus SQLite migrations for the repository's stdlib runner, with every column traced to an ADR "Stored data" line, every index proved by EXPLAIN QUERY PLAN, a privacy check that no column can hold person data, expand/backfill/contract templates that rebuild the table where SQLite cannot alter a column, and a real apply / no-op / revert round trip before anything reaches migrations/. Use when the owner says "data model for <slug>", "migrations for <slug>", "schema for <slug>" or "/data-model-builder <slug>" in a modular-monolith repository on SQLite whose results must stay team-level and public-safe. Needs docs/features/<slug>/PRD.md and sad.md with §6 flows; writes docs/features/<slug>/data-model.md and staged migrations, or another folder with --out-dir.
---

# data-model-builder

A standalone variant of the SDLC plugin's `generate-data-model` skill, tuned to this repository: SQLite
through the standard `sqlite3` module, plain `NNNN_<name>.up.sql` / `.down.sql` files applied by
`src/evidence_meter/platform/migrate.py`, five contexts that each own a table prefix, and a metrics tool
that must never store a value per person. Same flow as the plugin (gate, rules, read sources, aggregates,
keys, columns, indexes, design doc, migrations, seeds, drift, breaking changes, self-check, report); the
changes are listed at the end. It reads no file from the plugin.

## Inputs

- `<slug>`: kebab-case. Required: `docs/features/<slug>/PRD.md` and `docs/features/<slug>/sad.md`
  whose §6 ends with `### Coverage: US/AC → flows`. Missing SAD → stop, name `sad-builder` (or the
  plugin's `architecture-design`); missing coverage table → stop, name `complete-sequence-diagrams`. The
  flows are where indexes come from; without them every index is a guess.
- Read, in this order: SAD §5 context touch list (which tables, which prefix, which migration), every
  feature ADR's **Stored data** section (columns, keys, what a change costs), SAD §6 flows (each read or
  write step is a query), SAD §8 (ID strategy, time, privacy ledger), PRD §5 ACs (what must be shown or
  counted), `.claude/rules/migrations.md`, the live `migrations/`.
- Optional: `--out-dir <dir>` writes `<dir>/data-model.md` and `<dir>/migrations/` and touches nothing
  else (a comparison run); `--depth easy|medium` (default medium); `--promote` (step 11).

## Hard rules

- Synthetic and public data only: `team-alpha`, `PRJ-DEMO-1`, `metric-x`, states `Open`, `Doing`,
  `Done`. No organisation, person, project key, tracker state or metric code from a real setup.
- No column, index or seed that can hold a person: no assignee, author, reporter, user, email or name
  of a person. If an ADR or AC seems to need one, stop and ask; the answer is a team-level aggregate or a
  refusal, never a column. `scripts/check_migrations.py` fails on such names.
- A context writes only its own prefix (`collection_`, `computation_`, ...). No foreign key crosses a
  context: a reference to another context's row is a hash or natural-key column, as the SAD's ID
  strategy names it.
- Nothing goes into the live `migrations/` until `scripts/roundtrip.py` passes and the owner says yes.
- Every commit passes `make check` and follows the commit rule in AGENTS.md.

## Protocol

### 1. Gate
`test -f` both inputs and `grep -q '### Coverage: US/AC → flows' sad.md`. Read `.size` (absent → M).

### 2. Rules
Read `.claude/rules/migrations.md`. Absent → copy `templates/rules-migrations-sqlite.md` there and say so
in the reply. Present → it wins over this skill's defaults; list any difference in the report. Never
rewrite an existing rules file. With `--out-dir`, write no rules file: use the template as the rules and
say so in the report.

### 3. Storage ledger (the source of every table and column)
Build one table before designing anything: for each table in the SAD §5 touch list, the ADR(s) whose
Stored data names it, the flow steps that read or write it (quote the step text), and the ACs it serves.
A table with no ADR or flow → ask; an ADR Stored data line or a persist step with no table → ask. This
replaces the plugin's guess of entities from user stories.

### 4. Aggregates and keys
Each root table is an aggregate; children live in the same migration as their root. Primary key
`id INTEGER PRIMARY KEY`; identity is the natural `UNIQUE` key from SAD §8 (copy its column list
verbatim). If the SAD names no key for a table: ask at medium; at easy, add only the key a flow needs
(often none for a child table) and list it as an assumption.

### 5. Columns
From the ledger only. Types `INTEGER`, `REAL`, `TEXT`; every table `STRICT`; timestamps `TEXT` ISO 8601
UTC with `Z`, set by the app, named for the event (`imported_at`); hashes `TEXT` hex SHA-256; no
`DEFAULT`, no `updated_at`, no soft delete. A `CHECK` only when an Accepted ADR asks for it, with the ADR
number in a comment above it. Each column row in `data-model.md` names its source (ADR, AC or flow step).
Run the privacy check on the column list now, not at the end.

### 6. Indexes
One per query in the ledger. Write the query as SQL in `data-model.md` (`### Queries`), then name the
index that serves it. A `UNIQUE` key that already serves a query is the index; do not add a second. FK
columns need an index whose first column is the FK. No query → no index, except the FK rule, which says so.
A plan of `SEARCH ... USING INDEX` followed by `USE TEMP B-TREE FOR ORDER BY` is accepted when the
searched prefix returns a few rows (say how many in the doc); a full `SCAN` fails.

### 7. Design doc
Write `data-model.md` from `templates/data-model-template.md`: storage ledger, ER diagram, tables with
sources, queries with their index, privacy check, migrations, round-trip result, report. Validate the
`erDiagram`: `mmdc` if it runs, else the project's `mermaid` package (`mermaid.parse`), else a structural
lint. No `;` in Mermaid labels.

### 8. Migrations (staged)
Into `docs/features/<slug>/migrations/` (or `<out-dir>/migrations/`), named with the next free numbers
after the live tree: `NNNN_create_<context>_<root>.up.sql` + `.down.sql`. The SAD touch list decides the
split (one migration per context when it lists one); if it names the files, keep its numbers, add the
verb, and note the rename in the report. `CREATE ... IF NOT EXISTS`, `DROP ... IF EXISTS`, children dropped
before parents, no `BEGIN`/`COMMIT` (the runner wraps each file).

### 9. Seeds
Lookup data only, in its own migration with `INSERT ... ON CONFLICT DO NOTHING`. Test data never: tests
call the runner on `tmp_path` and insert synthetic rows. Say "no seeds" when there are none.

### 10. Changing an existing table
A NOT NULL column, rename, drop or type change on a table already in the live tree → three migrations
from `templates/expand-backfill-contract.md`: expand (add nullable, app writes both), backfill (`UPDATE`
with a `backfill-<column>.md` companion: rows, time, resumable `WHERE`, what its down loses), contract
(SQLite table rebuild, not `ALTER COLUMN`). Each is its own commit.

### 11. Checks, then promote
1. `uv run python <skill>/scripts/check_migrations.py <staged dir>`: naming, down reverses up, FK
   indexes, forbidden features, plus `STRICT`, context prefix, no cross-context FK, privacy names.
2. `uv run python <skill>/scripts/roundtrip.py --staged <staged dir> --queries <queries.sql>`: copies the
   live tree plus the staged files to a temp folder, runs the repository's runner: apply, apply again
   (must be a no-op), revert every staged file (structure must equal the live tree alone), apply again
   (structure must equal the first apply); then `EXPLAIN QUERY PLAN` for each query (a full `SCAN` fails).
3. Fix and repeat until both pass; on the second failure of the same kind, stop and report.
4. `--promote` (owner's yes): `git mv` the staged pairs to `migrations/`, add a test in
   `tests/test_migrate.py` that the live tree applies, reverts to empty and re-applies, then
   `make migrate` on a temp `EVIDENCE_METER_DB`: apply, no-op, `--revert` per file, apply.

### 12. Drift (when the context's `repo/` or `infra/` has code)
List every table and column name the code uses in SQL strings; report columns in code but not in the
schema, and the reverse. No code → say "drift skipped: no repo code yet".

### 13. Report and commit
The report is the last section of `data-model.md` (not a separate folder): files written, rules-file
differences, check results with commands, open questions, flags for the build (for example `PRAGMA
foreign_keys = ON` in the connection helper). Commit `[<lesson>] 04: data-model for <slug> via
data-model-builder`.

## Changed against the plugin's generate-data-model

- Defaults are SQLite and this runner: `NNNN_` names, `STRICT`, `INTEGER PRIMARY KEY` plus the SAD's
  natural key, app-set UTC text timestamps, no `DEFAULT` at all, table rebuild for contract, no
  `CONCURRENTLY`. The plugin keeps Postgres defaults that this runner and engine reject.
- Entities come from a storage ledger over SAD §5, ADR Stored data and flow steps, not from user stories.
- Every index has its query written as SQL and proved by `EXPLAIN QUERY PLAN`.
- Privacy and context-ownership checks are part of the self-check.
- The self-check and the round trip are scripts with exit codes, run against the real runner; the plugin
  describes them in prose.
- The report lives in `data-model.md`; promotion to `migrations/` is a step with a test, not deferred to
  `implement-tasks`.
- Removed: UUID v7, JSONB, Go fixtures, golang-migrate notes, the separate `_audit/` folder.
