---
id: T3
title: "Implement passes, median and cycle-time outcome in computation domain"
layer: "domain"
deps: ["T1"]
acs: ["AC-01", "AC-01b", "AC-04", "AC-08"]
files_hint: ["src/evidence_meter/computation/domain/", "tests/test_cycle_time.py", "tests/golden/"]
owner: "capstone owner"
estimate: "L"
status: "todo"
wave: 2
---

# T3 — Implement passes, median and cycle-time outcome in computation domain

## Why

[PRD AC-01, AC-01b, AC-04, AC-08](../PRD.md); [sad §6 flow 1](../sad.md); outcome rule [F1 ADR 0009](../adr/0009-computation-record-no-finished-passes-as-an-outcome.md); glossary Pass, Cycle time ([CONTEXT](../CONTEXT.md)).

## What

Pure functions: abstract transitions → passes (a reopen starts a pass; a pass counts in the UTC month of its done), median of durations, outcome `value` or `no_finished_passes`, state-map coverage returning the uncovered states. Golden snapshots with hand-computed values.

## Definition of Done

- [ ] unit tests for every AC-01, AC-01b, AC-04, AC-08 row of the [test plan](../test-plan.md) pass on golden data
- [ ] median of an even count and equal-timestamp tie-break covered
- [ ] `domain` imports only the standard library and `shared` (architecture test)
- [ ] `make check` passes

## Notes

Golden values are computed by hand in the fixture comments, never by the code under test.
