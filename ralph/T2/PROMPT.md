You run inside a loop: each turn starts with a fresh context, so everything you know comes from the
files. Work in small steps, leave notes, and stop when the done-criterion below holds.

## Context
Evidence Meter: Python 3.12, uv, standard library only for this task. Read before you change anything:
- `AGENTS.md` and `ARCHITECTURE.md`: conventions and the dependency rule (`platform` imports no context
  and no entry point).
- `docs/features/metric-computation/tasks/T2-platform-config-db.md`: the task and its Definition of Done.
- `tests/test_platform.py`: the acceptance test; it fixes the public interface you must provide.
- `src/evidence_meter/platform/migrate.py`: the existing platform module; follow its style (module
  docstring, type hints, `sqlite3` from the standard library).
- `var/ralph/T2/progress.md` if it exists: what earlier turns did and what was still failing.

## Task
Add `src/evidence_meter/platform/config.py` (`Config`, `load`) and `src/evidence_meter/platform/db.py`
(`connect`, `transaction`) so that `tests/test_platform.py` passes and `make check` stays green.

## DoD
1. `uv run pytest tests/test_platform.py -q` exits 0.
2. `make check` exits 0.
3. Only when both hold: write the file `DONE` in the repository root (word "DONE") with your
   file-writing tool, then stop.

Every turn, before you stop, append one line to `var/ralph/T2/progress.md`: what you changed and what
is still failing (paste the first failing line).

If the same failure survives three turns in `progress.md`, or the task needs something forbidden
below, write the reason to `var/ralph/T2/BLOCKED` and stop. If `var/ralph/T2/BLOCKED` already exists
when the turn starts, stop at once without changes.

## Do not

- Do not edit anything under `tests/`, `ralph/`, `.claude/`, `migrations/`, `docs/` or `pyproject.toml`; if a
  test fails, fix the code, not the test.
- Do not add dependencies; the standard library is enough.
- Do not commit, push, change branches or run `git reset` / `git checkout --`: the owner reviews the
  diff and commits.
- Do not read `~/.config/evidence-meter/`, `.env*` or any `*.private.*` file; `config.load` must build
  the default path without opening it.
- No data about people in code, comments or logs.
