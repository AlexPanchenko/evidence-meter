---
id: T4
title: "Read definitions file: versions, retirement, state maps, hashes"
layer: "app"
deps: ["T1", "T2"]
acs: ["AC-05", "AC-10"]
files_hint: ["src/evidence_meter/definitions/", "tests/test_definitions.py", "tests/fixtures/definitions.toml"]
owner: "capstone owner"
estimate: "M"
status: "todo"
wave: 2
---

# T4 — Read definitions file: versions, retirement, state maps, hashes

## Why

[PRD AC-05, AC-10](../PRD.md); [F1 ADR 0005](../adr/0005-definitions-read-a-toml-definitions-file.md); [sad §6 flow 2](../sad.md).

## What

`repo/` reads TOML with `tomllib`; `service/` validates, hashes the parsed version and the state map; `handler/` returns current or named version plus the team's state map, or `Refusal` `definitions_missing` / `definition_retired` (naming the current version).

## Definition of Done

- [ ] integration test with a temporary file: absent file → `definitions_missing`, retired v1 → `definition_retired` naming v2
- [ ] malformed file → usage error, not a refusal
- [ ] hashes are stable across key order in the file
- [ ] `make check` passes

## Notes

Synthetic fixture only (`cycle-time`, `team-alpha`). Never opens `~/.config/evidence-meter/`.
