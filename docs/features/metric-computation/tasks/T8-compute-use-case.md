---
id: T8
title: "Compute use case: coverage, key lookup, match or defect, record"
layer: "app"
deps: ["T3", "T7"]
acs: ["AC-01", "AC-03", "AC-04"]
files_hint: ["src/evidence_meter/computation/app/", "tests/test_compute_use_case.py"]
owner: "capstone owner"
estimate: "M"
status: "todo"
wave: 3
---

# T8 — Compute use case: coverage, key lookup, match or defect, record

## Why

[sad §6 flow 1](../sad.md) `alt` branches; [PRD AC-03](../PRD.md); [F1 ADR 0008](../adr/0008-computation-key-measurements-by-every-input.md).

## What

Given snapshot, version, state map and period: refuse `unmapped_states`, compute via domain, look up the key; new → record; same → match; different → defect.

## Definition of Done

- [ ] integration tests: match records nothing; defect records nothing and returns no value; unmapped states listed and nothing stored
- [ ] all three branches of flow 1 covered
- [ ] `make check` passes

## Notes

None.
