---
id: T1
title: "Add shared Team, Period, Refusal codes, records and event types"
layer: "domain"
deps: []
acs: ["AC-06", "AC-09"]
files_hint: ["src/evidence_meter/shared/", "tests/test_shared.py"]
owner: "capstone owner"
estimate: "M"
status: "todo"
wave: 1
---

# T1 — Add shared Team, Period, Refusal codes, records and event types

## Why

Contexts pass plain records through `entrypoints/` ([F1 ADR 0002](../adr/0002-entrypoints-orchestrate-a-run-with-shared-types.md)); refusals are typed results with a closed list ([F1 ADR 0007](../adr/0007-shared-return-refusals-as-typed-results.md)); a period closes by the UTC month ([F1 ADR 0006](../adr/0006-shared-store-utc-and-close-periods-by-utc-month.md)). Terms: [CONTEXT](../CONTEXT.md).

## What

`Team`, `Period` (`YYYY-MM`, `is_closed(now)` in UTC), `Refusal(code, message, details)` with the closed code list, frozen records for snapshot, definition version and state map, `events.py` with `TrackerSnapshotCollected` and `MetricComputed`. Data only, no context logic.

## Definition of Done

- [ ] unit tests: `Period.is_closed` is false at the last second of the month and true at the first second of the next (UTC); a malformed period is rejected
- [ ] the refusal code list equals F1 ADR 0007's list, checked by a test that parses the ADR
- [ ] `tests/test_architecture.py` passes: `shared` imports no context
- [ ] `make check` passes

## Notes

Updates the `shared/__init__.py` docstring (SAD §1 override).
