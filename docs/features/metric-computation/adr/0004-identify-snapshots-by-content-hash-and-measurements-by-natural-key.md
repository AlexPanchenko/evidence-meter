---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0004 — Identify snapshots by content hash and measurements by natural key

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

AC-03 and the reproducibility NFR require a re-run with the same snapshot and definition version to show the identical value, say it matches, and record nothing; a different result is a defect. The map records the ID strategy as UNKNOWN, to be decided with F1. Snapshots are imported from files (ADR 0001), so the same file may be imported twice.

## Decision drivers

- Reproducibility: 100% identical value and inputs on re-run (PRD §6 NFR, sad.md §1 QG-1).
- AC-03: a repeat records no second measurement; a mismatch reports a defect.
- Reference pattern: `platform/migrate.py`, where a repeat is a no-op that says so (PRD §1).

## Considered options

1. **Content hash and natural key** — A snapshot's id is the sha256 of its canonical content; re-importing the same content is a no-op. A measurement is unique on (team, period, definition id, definition version, snapshot id); a re-run compares with the stored row.
2. **Surrogate ids and a lookup** — Random UUIDs for snapshots and measurements, plus a query for the previous measurement of the same team, period and version, and a separate rule for 'same snapshot'.

## Decision outcome

**Chosen:** Option 1. Identity follows content, so 'same inputs' is a key lookup rather than a rule, and two imports of one file cannot become two snapshots.

## Consequences

**Positive**
- The re-run check is a single unique-key lookup and a comparison.
- Ids are stable across machines: the same file gives the same snapshot id anywhere.

**Negative**
- Canonical serialisation (key order, timestamp format) becomes part of the contract; changing it changes every id.
- A corrected re-export of the same month is a new snapshot; both are kept, so the Lead must pick which one to compute.

**Neutral**
- Measurements never update in place; history is not rewritten (US-07).

## Links

- PRD: [[../PRD.md]] §5 AC-03, §6 (reproducibility)
- SAD: [[../sad.md]] §4, §8 (ID strategy)
- Related ADR: [[0001-import-synthetic-snapshot-file-until-collection-adapter-exists]]; [[0003-orchestrate-compute-in-entrypoints-with-in-process-events]]
