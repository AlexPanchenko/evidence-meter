# Evidence Meter

Evidence Meter turns a written guide of engineering metrics into a tested tool. It collects data from an issue
tracker and Git, computes each metric from a versioned definition, refuses to report a value the data cannot
support, and drafts a monthly project page for a person to review and publish. Results are team-level only,
never per person. The repository holds generic tooling and synthetic or public data only: an organisation's own
metric codes, thresholds and identifiers live in a private definitions file outside git. It is built as the
capstone of the Agentic Engineering 3.0 course.

## Development

Python 3.12 with [uv](https://docs.astral.sh/uv/). `make sync` installs the environment; `make check` runs
the linters (ruff, the dependency rule, oxlint, the TypeScript check) and the tests (pytest, Vitest) and is
the command that proves a change.
