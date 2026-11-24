---
id: T6
title: "Serve the latest snapshot for a team and period"
layer: "infra"
deps: ["T5"]
acs: ["AC-07"]
files_hint: ["src/evidence_meter/collection/", "tests/test_collection_latest.py"]
owner: "capstone owner"
estimate: "S"
status: "todo"
wave: 3
---

# T6 — Serve the latest snapshot for a team and period

## Why

[PRD AC-07](../PRD.md); [sad §6 flows 1-2](../sad.md); index `idx_collection_snapshots_latest` ([data-model](../data-model.md)).

## What

Handler returns the latest snapshot by `imported_at` with its transitions in issue and time order, or `Refusal` `snapshot_missing`.

## Definition of Done

- [ ] integration test: none → `snapshot_missing`; another team's snapshot is not returned; two imports → the later one
- [ ] query uses the latest index (`EXPLAIN QUERY PLAN` asserted)
- [ ] `make check` passes

## Notes

Same lane as T5.
