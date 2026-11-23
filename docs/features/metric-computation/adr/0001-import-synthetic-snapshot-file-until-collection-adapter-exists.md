---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0001 — Import a synthetic snapshot file until Collection's tracker adapter exists

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

F1 computes cycle time from a closed snapshot, but Collection, the context that will read the issue
tracker, has no adapter yet (architecture-map: every context is empty). PRD §8 left open how F1 gets a
snapshot, due at this stage. The choice fixes what crosses the system boundary in F1 (sad.md §3) and how
much of Collection is built now.

## Decision drivers

- Offline: 0 network calls during computation (PRD §6 NFR).
- Reproducibility: 100% identical value and inputs on re-run (PRD §6 NFR, sad.md §1 QG-1).
- Public repository: synthetic data only; no tracker credentials or private state names in the dev loop (sad.md §2).
- Delivery window: design in week 1, build in week 2, one developer (sad.md §2).

## Considered options

1. **Synthetic snapshot file import** — a CLI command imports a snapshot file into Collection's store as an immutable snapshot; the tracker is not connected in F1.
2. **Minimal read-only tracker adapter now** — an adapter for one tracker's API in `collection/repo/`, giving real data from day one.

## Decision outcome

**Chosen:** Option 1. It keeps F1 at size M, offline and credential-free, and the golden-data tests use the
same import path as real runs; a real export can be imported from outside git when needed.

## Consequences

**Positive**
- Tests, demos and real use share one path: file → Collection store → Computation.
- No credentials, network or private tracker data in the repository or the dev loop.

**Negative**
- Real data needs a manual export step until the tracker adapter feature ships.
- The file format becomes Collection's input contract; the future adapter must produce the same snapshot shape.

**Neutral**
- Replacing the file with an adapter later changes only Collection's input side, not Computation.

## Links

- PRD: [[../PRD.md]] §8 (open question 1), §6 (offline, reproducibility)
- SAD: [[../sad.md]] §3
- Related ADR: repo [0003 persistence on SQLite](../../../adr/0003-persistence-sqlite.md)
