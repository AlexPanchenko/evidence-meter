---
id: T5
title: "Import a snapshot file into immutable collection tables"
layer: "app"
deps: ["T1", "T2", "T12"]
acs: ["AC-07"]
files_hint: ["src/evidence_meter/collection/", "tests/test_collection_import.py", "tests/fixtures/snapshots/"]
owner: "capstone owner"
estimate: "L"
status: "todo"
wave: 2
---

# T5 — Import a snapshot file into immutable collection tables

## Why

[sad §6 flow 3](../sad.md); [F1 ADR 0003](../adr/0003-collection-import-a-snapshot-file-as-an-immutable-snapshot.md); [F1 ADR 0004](../adr/0004-collection-drop-person-fields-at-import.md); [data-model](../data-model.md) collection tables; [cli.md import](../contracts/cli.md).

## What

Allow-list (issue key, from state, to state, UTC timestamp), canonical form and SHA-256, insert snapshot and transitions in one transaction, identical hash is a no-op; invalid file per T12's decision.

## Definition of Done

- [ ] integration test: person fields in the file never reach a table
- [ ] identical re-import stores nothing; a different file is a new snapshot
- [ ] hash unchanged by key order and whitespace in the file
- [ ] `make check` passes

## Notes

Shares `collection/` with T6 (serialized lane).
