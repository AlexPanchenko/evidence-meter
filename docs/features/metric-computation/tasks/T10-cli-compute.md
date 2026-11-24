---
id: T10
title: "Add the compute command with ordered checks and replies"
layer: "ports"
deps: ["T4", "T6", "T8", "T9"]
acs: ["AC-01", "AC-02", "AC-05", "AC-06", "AC-07", "AC-09", "AC-10"]
files_hint: ["src/evidence_meter/entrypoints/cli.py", "tests/test_cli_compute.py"]
owner: "capstone owner"
estimate: "L"
status: "todo"
wave: 4
---

# T10 — Add the compute command with ordered checks and replies

## Why

[cli.md compute](../contracts/cli.md) checks-in-order table and exit codes; [sad §6 flows 1-2](../sad.md).

## What

`evidence-meter compute <definition-id> --team --period [--version N] [--by team|person]`; checks in the contract's order, all before the first write; replies; dispatch `MetricComputed` after a new measurement.

## Definition of Done

- [ ] e2e in process for every AC-01..AC-10 row of the [test plan](../test-plan.md) marked e2e
- [ ] `--by person` refuses before the definitions file is opened (test asserts no open)
- [ ] output matches the contract's output fields
- [ ] `make check` passes

## Notes

Same lane as T9.
