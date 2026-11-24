---
id: T7
title: "Store measurements and state maps by measurement key"
layer: "infra"
deps: ["T1", "T2"]
acs: ["AC-01b", "AC-03", "AC-08"]
files_hint: ["src/evidence_meter/computation/infra/", "tests/test_computation_store.py"]
owner: "capstone owner"
estimate: "M"
status: "todo"
wave: 2
---

# T7 — Store measurements and state maps by measurement key

## Why

[F1 ADR 0008](../adr/0008-computation-key-measurements-by-every-input.md); [F1 ADR 0009](../adr/0009-computation-record-no-finished-passes-as-an-outcome.md); [data-model](../data-model.md) computation tables.

## What

Find a measurement by the 7-column key; insert a measurement and its state map (if new) in one transaction; rows are never updated.

## Definition of Done

- [ ] integration test on a migrated temporary database: find by key, insert, second insert of the same key rejected
- [ ] `no_finished_passes` stored with an empty value; a value with that outcome rejected by the CHECK
- [ ] an earlier period's row is unchanged after inserting a later one
- [ ] `make check` passes

## Notes

None.
