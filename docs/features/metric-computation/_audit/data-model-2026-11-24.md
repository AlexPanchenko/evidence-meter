# Audit: generate-data-model on metric-computation, 2026-11-24

Plugin `sdlc` 4.10.4, skill `generate-data-model`, greenfield mode, after `complete-sequence-diagrams`
(commit `09fc051`). Owner's choices before the run: SQLite dialect and `NNNN` names; `INTEGER PRIMARY
KEY`; keep F1 ADR 0009's CHECK; breaking change as a staged exercise only.

## Generated files

- `.claude/rules/migrations.md`: bootstrapped from the plugin's baseline, then edited for SQLite (each
  change marked "baseline:" in the file).
- `data-model.md`: ER diagram (parsed with the project's `mermaid` package), 4 tables, 6 indexes with
  the query each serves.
- Staged in `migrations/` of this folder: `0002_create_collection_snapshots`,
  `0003_create_computation_measurements` (up + down). The plugin leaves promotion to `implement-tasks`;
  here they move to the live `migrations/` in the next commit, because the lesson asks for the
  apply / no-op / revert proof now and no code reads these tables yet.
- `migrations/_exercise/`: `0004_expand_...`, `0005_backfill_...`, `0006_contract_...` and
  `backfill-source.md`. Never promoted.

## Convention divergences (course default → this repo)

| Course default | Here | Why |
|---|---|---|
| `YYYYMMDDhhmmss_` names | `NNNN_<verb>_<entity>` | `platform/migrate.py` accepts only `\d{4}_[a-z0-9_]+`; one owner on `main` |
| UUID v7 app-side | `id INTEGER PRIMARY KEY` + natural `UNIQUE` key | single local writer; no `uuid7` in Python 3.12 |
| `TIMESTAMPTZ NOT NULL DEFAULT now()` | `TEXT NOT NULL`, app-set ISO 8601 UTC `Z`, no DEFAULT | SQLite has no `now()`; injected clock for golden tests (F1 ADR 0006) |
| `created_at` | `imported_at`, `computed_at`, `recorded_at` | named for the event the ADRs and flows use |
| `VARCHAR(N)` | `TEXT` in `STRICT` tables | SQLite ignores the bound; STRICT enforces the type |
| `JSONB` for opaque payload | `TEXT` canonical JSON (`canonical_map`) | the stored form is what gets hashed |
| no CHECK | one CHECK on `computation_measurements` | Accepted F1 ADR 0009, commented in the SQL |
| `CREATE INDEX CONCURRENTLY` | plain `CREATE INDEX IF NOT EXISTS` | not in SQLite; no concurrent writers |
| `SET NOT NULL` in contract | table rebuild | SQLite cannot alter a column |
| one migration per entity | one per context (2 tables each) | matches SAD §5 touch list |

## Drift

- **Schema vs source:** skipped. `collection/repo/` and `computation/infra/` have no code yet, so
  there are no fields to compare. Run `--drift-only` after S9 builds the repos.
- **Model vs spec:** every table in SAD §5 has a migration; every table traces to an ADR. No table
  without an origin. SAD §5 names the files without the verb (`0002_collection_snapshots`); the files
  use `0002_create_...` per the rules (cosmetic, SAD wording to update with the next SAD touch).

## Breaking changes decomposed

None in F1. The exercise adds NOT NULL `collection_snapshots.source` in three steps. It was proved on a
scratch database with the real runner: up (6 migrations), no-op, down ×3, structure equal to 0002 + 0003
alone, up again equal to the first up, then down ×6 to an empty schema. One seeded row survived the
round trip.

## Self-check (4 points)

Naming, down reverses up, FK indexes, forbidden features: 4/4 pass on 5 up files (scratch script). The
same script on a broken copy reported all four kinds of fault.

## Checks beyond the plugin

- Constraints on a scratch DB: the 7-column UNIQUE rejects a second row; the CHECK rejects value with
  `no_finished_passes`, NULL with `value`, and an unknown outcome; STRICT rejects text in an INTEGER
  column; FKs reject orphans **only with `PRAGMA foreign_keys = ON`** (without it, an orphan transition
  was accepted) → `platform/db.py` must set it.
- `EXPLAIN QUERY PLAN` for the five F1 queries: each uses its index.

## TBDs

None in `data-model.md`. Open: whether `import` refuses a period that is not closed (no schema impact).
