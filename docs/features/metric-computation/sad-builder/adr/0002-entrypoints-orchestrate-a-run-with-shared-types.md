---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0002 — Orchestrate a run in entrypoints with shared types and in-process events

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** entrypoints
- **Gate:** I ✓ M ✓ A ✓ D ✗ → 3/4

## Context

F1 is the first feature that crosses contexts: a compute run needs a definition version and state map
(Definitions), a snapshot (Collection) and a formula (Computation). bc-map says contexts talk through events
wired in `entrypoints/`, but no event type or dispatcher exists yet (architecture map). The Lead asks for
one team and one period and expects a value or a refusal back in the same command (PRD AC-01, AC-04..AC-10).

## Decision drivers

- All-or-nothing: 0 partial records after a refused or failed run (PRD §6).
- Dependency rule: a context imports only itself, `shared` and `platform` (AGENTS.md, repo ADR 0002).
- A refusal is a result the Lead reads, not a lost message (ARCHITECTURE.md).

## Considered options

1. **Orchestrate in entrypoints** — the `compute` command calls each context's handler in order, passes
   `shared` types (`Team`, `Period`, snapshot and definition records), and publishes `TrackerSnapshotCollected`
   (after import) and `MetricComputed` (after a new measurement) to an in-process dispatcher in `entrypoints/`.
2. **Full event chain** — import publishes `TrackerSnapshotCollected`; Computation computes when it hears it.

## Decision outcome

**Chosen:** orchestrate in entrypoints. Option 2 has no channel to return a refusal to the Lead who asked,
and it computes on import rather than on the Lead's request for a period.

## Consequences

**Positive**
- All checks run before the first write in one place; the store is unchanged on every refusal.
- `shared/events.py` and the dispatcher exist, so Evidence Guard can subscribe to `MetricComputed` later.

**Negative**
- The run order lives in `entrypoints/`; a later batch run (all teams) must reuse this orchestration, not
  copy it.
- The dispatcher has no listener in F1; its first real test comes with Evidence Guard.

**Neutral**
- Definitions events (`DefinitionVersionPublished`, `DefinitionVersionRetired`) are not published in F1:
  the file is read at run time (SAD §11 accepted debt).

## Links

- PRD: [[../../PRD.md]] §5 (AC-01, AC-04..AC-10), §6 (all-or-nothing)
- SAD: [[../sad.md]] §4, §5, §6
- Related ADR: [[0001-entrypoints-serve-f1-through-the-cli-only]]; repo ADR 0002
