---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0003 — Orchestrate compute in entrypoints with in-process events

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

A compute run needs a snapshot (Collection), a definition version with a state map (Definitions) and the formula (Computation). The repo forbids one context importing another; only `entrypoints/` wires contexts, and contexts talk through events (bc-map). The scaffold has no event types and no dispatcher yet (architecture-map), so F1 defines both.

## Decision drivers

- Dependency rule enforced by `tests/test_architecture.py` (sad.md §2).
- All-or-nothing: 0 partial records after a refused or failed run (PRD §6 NFR, sad.md §1 QG-3).
- One developer, one metric: the simplest wiring that keeps contexts separate.

## Considered options

1. **Entrypoint orchestration** — The compute command in `entrypoints/` calls the Definitions and Collection handlers, maps their results into Computation's own input types, runs the use case, and publishes `MetricComputed` to an in-process dispatcher.
2. **Event-driven local copies** — Import publishes `TrackerSnapshotCollected` with the snapshot; Computation stores its own copy and compute reads only Computation's tables.

## Decision outcome

**Chosen:** Option 1. It satisfies the dependency rule with synchronous, testable calls and one snapshot copy; Computation sees only its own input types (an anti-corruption mapping in `entrypoints/`), so it never depends on another context's classes.

## Consequences

**Positive**
- One place shows the whole run; refusals stop it before anything is written.
- Computation's domain stays independent of Collection's and Definitions' shapes.

**Negative**
- `entrypoints/` grows into a coordinator; the all-teams run (PRD approach C) may need its own application service.
- The in-process dispatcher has no listeners in F1, so `MetricComputed` is published but not yet consumed.

**Neutral**
- Moving to event-driven copies later means adding listeners and a replay, not changing the formulas.

## Links

- PRD: [[../PRD.md]] §5 AC-04, AC-05, AC-07, AC-10 (refusals before any write)
- SAD: [[../sad.md]] §4, §5
- Related ADR: [[0004-identify-snapshots-by-content-hash-and-measurements-by-natural-key]]; repo [0002 modular monolith](../../../adr/0002-modular-monolith.md)
