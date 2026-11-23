# Repository patterns prd-builder uses

Read in step 1. The PRD stays product-level in §1-§5; these patterns fill §6, §9, §10 and §11 and tell the
critic what this repository considers a leak.

## Contexts, their words and their states

From `docs/bc-map.md`. A term in an AC must come from the feature's `CONTEXT.md` or this table.

| Context | Owns | State words |
|---|---|---|
| Collection | Source, Snapshot, Issue, IssueState, Commit | IssueState (tracker workflow state); Snapshot is immutable once collected |
| Definitions | MetricDefinition, DefinitionVersion, Formula, MinimumData | DefinitionVersion: published → retired (`DefinitionVersionPublished`, `DefinitionVersionRetired`); a retired version produces no new values, old values keep naming it |
| Computation | Measurement, Input, FormulaId | Measurement is recorded once per team, period and definition version; a repeat with the same inputs matches it |
| Evidence Guard | Verdict, RefusalReason, Coverage, Threshold | Verdict: accepted or refused with a reason (`ValueAccepted`, `ValueRefused`) |
| Reporting | MonthlyPage, PageState, Review, Publication | PageState: drafted → reviewed → published; only a reviewed page can be published |

`Team` and `Period` are shared identifiers. Event flow: `ReportingPeriodClosed` → Collection →
`TrackerSnapshotCollected` / `GitHistoryCollected` → Computation → `MetricComputed` → Evidence Guard →
`ValueAccepted` / `ValueRefused` → Reporting; `CollectionFailed` → Reporting.

## Refusal is a Verdict, not an error

- **Result**: the system records and shows something, including a stated «no value» (an empty median is a
  formula result, not a refusal).
- **Refusal**: Evidence Guard returns a `Verdict` with a `RefusalReason` (too little data, low coverage,
  a per-person breakdown). The page shows the refusal and its reason. No error code.
- **Error**: the request cannot run (missing definitions file, unmapped states, period not closed, no
  snapshot). The system stops, records nothing and tells the actor what to fix.

Only errors get codes and only errors fall under the all-or-nothing NFR. Tag every AC with its class; an AC
that records something must not sit under a story about «why nothing was produced».

## Error-code convention

- Form: `<context>.<error_name>`, snake_case, context from the table above in snake_case
  (`collection`, `definitions`, `computation`, `evidence_guard`, `reporting`).
- Name the condition, not the HTTP outcome: `computation.unmapped_states`, `definitions.file_missing`,
  `collection.snapshot_missing`, `computation.period_not_closed`, `definitions.version_retired`.
- Generic transport codes stay unprefixed and belong to the entry point: `not_found`,
  `method_not_allowed`, `http_error` (see `entrypoints/api.py`).
- API shape: `{"error": {"code", "message"}}`. The CLI prints the same message and exits non-zero.
- Codes appear in PRD §10 only, never in §5.

## NFR defaults for this stack

A local, single-user tool: a command line and an API on 127.0.0.1, a file database, pure formulas. Start
from these; change a target only with a reason.

| Aspect | Default target | Measurement |
|---|---|---|
| Command run time, one team and period | ≤ 10 s for a 5,000-issue snapshot on a developer laptop | timed test on a synthetic snapshot |
| API read latency p95 | ≤ 200 ms on 127.0.0.1 for one team and period | timed API test, 100 requests |
| Reproducibility | 100% identical value and inputs on re-run | re-run test over golden data |
| Golden data | every formula has hand-computed expected values | golden-data tests in `make check` |
| Offline | 0 network calls in computation and in `make check` | network-blocked test (SPEC 8) |
| Per-person data | 0 per-person fields in output, records, logs, page, API | output scan test (SPEC 5) |
| All-or-nothing | 0 partial records after any error | store-unchanged test per error AC |
| Migration | every forward migration has a rollback that restores the schema | up/down test |
| Availability, throughput | N/A until the API serves data to other machines (ADR 0004) | — |

## Words that do not belong in §1-§5

Stack (ADR 0001, 0003): Python, uv, FastAPI, argparse, SQLite, React, Vite, TypeScript, migration,
endpoint, p95, p99. They may appear in §6, §10 and §11 when the row needs them.

## Reference modules

- `platform/migrate.py`: applying again is a no-op that says «nothing pending»; each change is all-or-nothing;
  a refusal lists the offending items. Good source for idempotency, all-or-nothing and «list what to fix» ACs.
- `entrypoints/api.py`: the error envelope.
- `tests/test_architecture.py`: the dependency rule a cross-context AC must respect (contexts talk through
  events, never imports).
