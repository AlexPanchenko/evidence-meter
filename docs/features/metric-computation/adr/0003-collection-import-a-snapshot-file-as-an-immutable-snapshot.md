---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0003 — Import a snapshot file as an immutable stored snapshot

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** collection
- **Gate:** I ✓ M ✓ A ✓ D ✓ → 4/4

## Context

PRD §8 asks how F1 gets a closed snapshot before Collection reads a tracker; the default was a synthetic
stored snapshot. A measurement must point at inputs that cannot change (SPEC acceptance criterion 1,
PRD AC-03), and AC-07 needs a way to say "no snapshot for this team and period".

## Decision drivers

- Reproducibility: 100% identical value and inputs on re-run (PRD §6).
- Offline: 0 network calls during computation (PRD §6).
- Standard library first (AGENTS.md).

## Considered options

1. **Import a JSON file into `collection_*` tables** — immutable rows plus a SHA-256 hash of the canonical
   form (the stored fields only, keys sorted, timestamps in UTC); identical re-import is a no-op; a
   different file for the same team and period is a new snapshot; compute uses the latest.
2. **Read the file at compute time** — no stored snapshot; the file path is the input.

## Decision outcome

**Chosen:** option 1. It gives a measurement a fixed snapshot hash to point at, keeps Collection the owner of
snapshots (bc-map), and lets later tracker adapters write into the same tables.

## Consequences

**Positive**
- AC-07 is a lookup: no stored snapshot → refusal `snapshot_missing`.
- A re-run reads the same rows; the hash proves it.

**Negative**
- The JSON shape becomes the contract later tracker adapters must map into.
- "Latest snapshot wins" means a corrected import changes which snapshot compute reads; the measurement
  key carries the hash, so the old measurement stays and a new one is recorded (F1 ADR 0008).

**Neutral**
- Synthetic files live in `tests/`; a Lead's real file stays outside the repo.

**Stored data**
- `collection_snapshots` (team, period, hash, imported_at) and `collection_issue_transitions` (snapshot,
  issue key, from state, to state, at). Changing the canonical form changes every hash: a migration plus a
  re-hash and re-check of golden data.

## Links

- PRD: [[../PRD.md]] §8 (open question 1), AC-03, AC-07
- SAD: [[../sad.md]] §4, §5, §8
- Related ADR: [[0004-collection-drop-person-fields-at-import]]; [[0008-computation-key-measurements-by-every-input]]
