# data-model-builder (draft)

Own variant of the SDLC plugin's `generate-data-model` skill (homework m06-l05, hard level). The draft
lives here because Claude cannot write to `.claude/skills/`; the owner installs it:

    mkdir -p .claude/skills && cp -R docs/skills-draft/data-model-builder .claude/skills/

Files: `SKILL.md` (flow; what changed against the plugin is at its end),
`templates/data-model-template.md` (storage ledger, tables with sources, queries with plans, privacy
check, report), `templates/rules-migrations-sqlite.md` (bootstrapped as `.claude/rules/migrations.md`
when absent), `templates/expand-backfill-contract.md` (SQLite: drop column, lossy backfill down, table
rebuild for contract), `scripts/check_migrations.py` (static self-check, exit code),
`scripts/roundtrip.py` (real runner on a temp copy: apply, no-op, revert, re-apply, structure compare,
`EXPLAIN QUERY PLAN` per query).

Both scripts were tried on the plugin's output before the run: `check_migrations.py` gives 0 findings on
`migrations/` plus the plugin run's exercise and 9 on a deliberately broken copy (exit 1);
`roundtrip.py` passes the round trip and fails a planted query that scans a table.

## Run: comparison with the plugin's generate-data-model

Same feature (`metric-computation`), same inputs. The plugin's skill, run in the main session with the
owner's four choices (SQLite + `NNNN`, `INTEGER PRIMARY KEY`, keep F1 ADR 0009's CHECK, staged
exercise), gave [data-model.md](../../features/metric-computation/data-model.md), the
[audit](../../features/metric-computation/_audit/data-model-2026-11-24.md) and `migrations/0002`,
`0003` (1277 words, 6 indexes). data-model-builder at easy depth, in a clean-context subagent that was
told not to open the plugin run's files (an instruction, not a sandbox block), gave
[skill-run/data-model.md](../../features/metric-computation/skill-run/data-model.md) and staged
`skill-run/migrations/` (1955 words, 5 indexes). Both: `check_migrations.py` 0 findings,
`roundtrip.py` pass.

I replaced the plugin's Postgres defaults with this repo's SQLite and runner rules, added a storage
ledger (SAD §5 table × ADR Stored data × quoted flow step) as the only source of columns, privacy and
context-ownership checks, and turned the prose self-check and round trip into scripts with exit codes;
I removed UUID v7, JSONB, Go fixtures and the separate `_audit/` folder. The schema came out the same
(4 tables, the 7-column measurement key, the ADR 0009 CHECK, no cross-context FK), because the
SAD-builder ADRs already state their stored data; the gain is in how each choice is proved. Index
quality gained most: every index has its query as SQL and an `EXPLAIN QUERY PLAN` line, which also
dropped the plugin run's `idx_collection_snapshots_latest`, since the unique `(team, period, hash)`
prefix serves "latest" with a small sort. Column names gained a little (`version_number`,
`version_hash`, as SAD §8 words them). The step I reworked is the plugin's self-check: the four prose
checks became `check_migrations.py` (plus STRICT, prefix, cross-context FK, person fields), and the
staged-then-`implement-tasks` promotion became a round trip on the real runner plus a pinning test
before `migrations/`. For this repository data-model-builder is the closer fit; the plugin's output
needed four owner decisions up front to run on SQLite at all.

## Changed after the run

The run listed 7 unclear points. Fixed in `SKILL.md`: `--out-dir` writes no rules file (step 2); easy
depth picks the minimal key when the SAD names none (step 4); a SEARCH plus a temp sort passes, a full
SCAN fails (step 6); the SAD touch list decides the migration split and its names keep their numbers
(step 8). Not changed: `stage: "07"` in the template (the plugin's stage id); the `mktemp` note was a
run condition, not a skill step. The canonical F1 schema stays the plugin run's `migrations/0002`,
`0003`; the skill run stays in `skill-run/` as evidence.
