---
id: T12
title: "Close the contract deferrals and the SAD doc debt"
layer: "docs"
deps: []
acs: ["AC-07"]
files_hint: ["docs/features/metric-computation/PRD.md", "docs/features/metric-computation/adr/0007-shared-return-refusals-as-typed-results.md", "docs/features/metric-computation/sad.md", "ARCHITECTURE.md", "docs/bc-map.md"]
owner: "capstone owner"
estimate: "S"
status: "todo"
wave: 1
---

# T12 — Close the contract deferrals and the SAD doc debt

## Why

[api-sync-report](../contracts/api-sync-report.md) Deferrals 1-3 and the SAD §11 accepted debt; the `contract-builder` run also found that SAD §8 forbids private names on stderr while refusal replies need them.

## What

Owner decisions, then edits: an AC for an unreadable or malformed snapshot file and `snapshot_invalid` in ADR 0007; whether `import` refuses a period that is not closed; §6 branches for usage errors; SAD §8 logging line split into logs vs terminal replies; ARCHITECTURE.md layout and event table, bc-map map.

## Definition of Done

- [ ] `api-sync-report.md` Deferrals 1-3 are closed or carry an owner decision
- [ ] `/sdlc:api-forge metric-computation --reconcile` reports PASS
- [ ] `make diagrams` renders changed Mermaid (run by the owner)
- [ ] `make check` passes

## Notes

Blocks T5 (import must know its refusal). KPI 3 measurement stays deferred to a later feature (owner, 2026-11-24).
