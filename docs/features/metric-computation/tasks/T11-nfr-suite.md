---
id: T11
title: "Add the NFR suite: all-or-nothing, person scan, offline, run time, smoke"
layer: "tests"
deps: ["T10"]
acs: ["AC-02", "AC-09"]
files_hint: ["tests/test_all_or_nothing.py", "tests/test_person_fields.py", "tests/test_offline.py", "tests/test_compute_runtime.py", "tests/test_cli_smoke.py"]
owner: "capstone owner"
estimate: "M"
status: "todo"
wave: 5
---

# T11 — Add the NFR suite: all-or-nothing, person scan, offline, run time, smoke

## Why

[PRD §6](../PRD.md) NFRs; [sad §10](../sad.md) QG-1..QG-5; [test plan](../test-plan.md) NFR section.

## What

Parametrised refusal walk with a byte-identical store check; scan of stdout, stderr, rows and logs for person fields; compute with sockets blocked; generated 5,000-issue snapshot under 10 s; one installed-command smoke test.

## Definition of Done

- [ ] all five suites pass in `make check`
- [ ] the run-time test fails when the limit is set below the measured time (checked once by hand)
- [ ] `make check` passes

## Notes

Test file names are the ones SAD §10 names.
