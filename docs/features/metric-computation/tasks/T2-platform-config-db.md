---
id: T2
title: "Add platform config and one-transaction database helper"
layer: "infra"
deps: []
acs: []
files_hint: ["src/evidence_meter/platform/config.py", "src/evidence_meter/platform/db.py", "tests/test_platform.py"]
owner: "capstone owner"
estimate: "S"
status: "todo"
wave: 1
---

# T2 — Add platform config and one-transaction database helper

## Why

SAD §5 touch list and §8 Configuration and Transactions; [data-model flags](../data-model.md) require `PRAGMA foreign_keys = ON`.

## What

`config.py` reads `EVIDENCE_METER_DB` and `EVIDENCE_METER_DEFINITIONS` (default `~/.config/evidence-meter/definitions.toml`); `db.py` opens a connection with foreign keys on and gives one transaction per command.

## Definition of Done

- [ ] integration test: a transition for a missing snapshot is rejected (foreign keys on)
- [ ] integration test: an error inside the transaction leaves the database unchanged
- [ ] config test reads both variables and the default path without reading the real file
- [ ] `make check` passes

## Notes

Never reads the private definitions file in tests; uses a temporary path.
