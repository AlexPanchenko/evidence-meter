---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0004 — Drop person fields at import

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** collection
- **Gate:** I ✓ M ✗ A ✓ D ✓ → 3/4

## Context

The snapshot may carry assignees and authors; F1 reads states and timestamps only (PRD §6.1). The tool must
never become a ranking of people (SPEC non-goals, AGENTS.md), and AC-09 requires that nothing per person is
recorded, shown or logged.

## Decision drivers

- 0 per-person fields in command output, records or logs (PRD §6).
- Security review required for a new boundary around person data (PRD §6.1).

## Considered options

1. **Drop at import** — Collection's import keeps issue key, state transitions and timestamps; every other
   field of the file is ignored and never stored or logged.
2. **Store the full file, filter on every output** — person fields in SQLite, each output path filters them.

## Decision outcome

**Chosen:** drop at import. One allow-list at one boundary is testable; option 2 needs a filter on every
present and future output.

## Consequences

**Positive**
- The privacy test checks one place (the import allow-list) plus the outputs, which then cannot hold a
  person field.

**Negative**
- A later feature that needs authors (Git coverage) adds a new, reviewed field; dropped data cannot be
  recovered from stored snapshots, only by re-importing.

**Neutral**
- Issue keys are kept: they identify work, not people. They appear in no F1 output.

**Stored data**
- The canonical form hashed by F1 ADR 0003 contains only the allowed fields, so adding a field later changes
  every new hash.

## Links

- PRD: [[../PRD.md]] §6.1, AC-02, AC-09
- SAD: [[../sad.md]] §4, §8 (privacy ledger)
- Related ADR: [[0003-collection-import-a-snapshot-file-as-an-immutable-snapshot]]
