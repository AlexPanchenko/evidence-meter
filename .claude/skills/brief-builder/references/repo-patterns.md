# Repository patterns brief-builder uses as reference

Read in step 0. The brief stays product-level; these patterns help pick realistic options, name the
neighbouring work in feasibility, and recognise words that do not belong in a brief.

## Contexts and their words
The repository is a modular monolith with one package per context; each context owns its terms
(see `docs/bc-map.md`). A new domain word in an interview is checked against this table first; if a
context already owns it, the brief reuses that meaning.

| Context | Owns |
|---|---|
| Collection | Source, Snapshot, Issue, IssueState, Commit |
| Definitions | MetricDefinition, DefinitionVersion, Formula, MinimumData |
| Computation | Measurement, Input, FormulaId |
| Evidence Guard | Verdict, RefusalReason, Coverage, Threshold |
| Reporting | MonthlyPage, PageState, Review, Publication |

`Team` and `Period` are shared identifiers.

## Refusal is a result, not an error
A value the data cannot support comes back as a `Verdict` with a `RefusalReason` (too little data, low
coverage, a per-person breakdown). In a brief this means: "the tool declines to show a number and says
why" is a product behaviour to design, not a failure to hide. API errors use one shape,
`{"error": {"code", "message"}}`, with snake_case codes; a brief never names codes, the PRD does.

## Contexts talk through events
`ReportingPeriodClosed` → Collection → `TrackerSnapshotCollected` / `GitHistoryCollected` → Computation →
`MetricComputed` → Evidence Guard → `ValueAccepted` / `ValueRefused` → Reporting. A feature that needs one
context to call another is a boundary question, so it goes to §15, not into an approach.

## Words banned in a brief here (stack, from ADR 0001 and 0003)
Python, uv, FastAPI, argparse, SQLite, React, Vite, TypeScript, migration, endpoint, p95, p99.

## Adjacent work for feasibility
Cite paths or commits: `platform/migrate.py` (migration runner), `tests/test_architecture.py`
(dependency rule), `entrypoints/cli.py` and `entrypoints/api.py`, `docs/features/<slug>/` of earlier features.
