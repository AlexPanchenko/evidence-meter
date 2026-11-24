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
