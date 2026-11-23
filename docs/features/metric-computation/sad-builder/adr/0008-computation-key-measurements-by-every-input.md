---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0008 — Key measurements by every input

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** computation
- **Gate:** I ✓ M ✗ A ✓ D ✓ → 3/4

## Context

AC-03 says a re-run with the same snapshot and definition version shows the identical value, records nothing
new, and reports a defect if the result differs. A measurement depends on the snapshot, the definition
version, the team's state map and the period (CONTEXT "Measurement", "State map"). If an input that can
change is missing from the identity, a legitimate change looks like a defect.

## Decision drivers

- Reproducibility: 100% identical value and inputs on re-run (PRD §6).
- A measurement names its definition id, version and inputs (SPEC criterion 2, CONTEXT invariant).
- Old measurements stay unchanged (AC-08, AC-10).

## Considered options

1. **Key by every input** — unique key: team, period, definition id, version number, version hash, snapshot
   hash, state-map hash. A changed input gives a new record; the same key with a different value is a defect.
2. **Key by team, period, definition id and version** — hashes stored as columns; a different snapshot or
   state map under the same key is reported as a defect.

## Decision outcome

**Chosen:** key by every input. Re-importing a corrected snapshot or extending a state map after
`unmapped_states` is normal work, not a defect; only the formula can make the same inputs give a different
value.

## Consequences

**Positive**
- The AC-03 defect means exactly one thing: the formula changed behaviour for the same inputs.
- No record is ever updated; history stays as computed.

**Negative**
- Several measurements can exist for one team and period. "Current" is a read rule (latest snapshot,
  current version and state map) that Evidence Guard and Reporting must follow; F1 shows the one it just
  computed or matched.

**Neutral**
- Hashes are SHA-256 over canonical forms: snapshot (F1 ADR 0003), version and state map as parsed from the
  file (F1 ADR 0005).

**Stored data**
- `computation_measurements` with a unique index over the seven key columns, plus outcome, value, passes
  counted and issues excluded; `computation_state_maps` keeps each state map used, by hash, so the
  measurement stays traceable after the Lead edits the definitions file (critic resolution, PRD US-02).
  Changing the key later means a migration and a decision about duplicate rows.

## Links

- PRD: [[../../PRD.md]] AC-02, AC-03, AC-08, AC-10
- SAD: [[../sad.md]] §6 flow 1, §8 (ID strategy)
- Related ADR: [[0003-collection-import-a-snapshot-file-as-an-immutable-snapshot]]; [[0005-definitions-read-a-toml-definitions-file]]
