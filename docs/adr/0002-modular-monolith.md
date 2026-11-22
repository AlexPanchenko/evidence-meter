---
status: Accepted
date: 2026-11-22
---

# ADR 0002: Style — modular monolith, one package per bounded context

## Context and problem statement

`docs/bc-map.md` fixed five contexts and a structure for each. One person builds the tool; boundaries
must hold without the cost of separate services.

## Decision drivers

- The boundary is the expensive decision; the folder layout must make it visible.
- A boundary that no test checks erodes.

## Considered options

1. One package per context under `src/evidence_meter/`, structure per bc-map, imports checked by a test.
2. Layer-first packages (`handlers/`, `services/`, `repos/`) shared by all contexts.
3. Separate services per context.

## Decision outcome

Option 1. Computation uses domain/app/infra (pure formulas tested without I/O); the others use
handler/service/repo. A context imports only `shared`, `platform` and itself; `entrypoints` (CLI, API)
wire contexts through events. `tests/test_architecture.py` (standard library `ast`) enforces the rule and
runs in `make lint`.

### Consequences

- Good: a context can move to its own service later by its package edge.
- Bad: empty layer packages exist before any code; they are placeholders with docstrings only.
