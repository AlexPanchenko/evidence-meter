---
id: T9
title: "Add the import command and the in-process event dispatcher"
layer: "ports"
deps: ["T5"]
acs: ["AC-07"]
files_hint: ["src/evidence_meter/entrypoints/cli.py", "src/evidence_meter/entrypoints/dispatch.py", "tests/test_cli_import.py"]
owner: "capstone owner"
estimate: "S"
status: "todo"
wave: 3
---

# T9 — Add the import command and the in-process event dispatcher

## Why

[cli.md import](../contracts/cli.md); [F1 ADR 0002](../adr/0002-entrypoints-orchestrate-a-run-with-shared-types.md) dispatcher.

## What

`evidence-meter import <file> --team --period`; replies and exit codes per the contract; dispatch `TrackerSnapshotCollected` after a new snapshot only.

## Definition of Done

- [ ] e2e in process: new, identical and invalid files give the contract's replies and exit codes
- [ ] event dispatched once for a new snapshot, never for the identical case
- [ ] `make check` passes

## Notes

Shares `cli.py` with T10 (serialized lane).
