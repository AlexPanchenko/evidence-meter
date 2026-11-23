---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0005 — Drop person fields at snapshot import

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

A tracker export may carry assignees and authors (PRD §6.1). F1 needs only issue keys, states and timestamps. The tool must never show, record or log a value per person (SPEC non-goals, AC-09), and the security review covers the new boundary around person data.

## Decision drivers

- Team-level only: 0 per-person fields in output, records or logs (PRD §6 NFR, sad.md §1 QG-2).
- AC-09: a person breakdown is refused and nothing per person is recorded, shown or logged.
- Public repository and security review (sad.md §2).

## Considered options

1. **Drop at import** — Collection's import keeps issue key, state changes and timestamps and discards person fields before anything is stored.
2. **Store and filter at output** — Keep person fields in the stored snapshot and filter them out at every output path.

## Decision outcome

**Chosen:** Option 1. Data that is never stored cannot leak through a later bug; the output-scanning test then guards against regressions instead of being the only control.

## Consequences

**Positive**
- AC-09 and the per-person NFR hold by construction.
- The security review checks one place: the import mapping.

**Negative**
- A future metric that needs authors must add the field deliberately, with a new ADR and an Evidence Guard rule.

**Neutral**
- Team size (PRD §8 open question 3) can still be supplied by the definitions file later without storing people.

## Links

- PRD: [[../PRD.md]] §5 AC-09, §6.1
- SAD: [[../sad.md]] §4, §8 (privacy)
- Related ADR: [[0001-import-synthetic-snapshot-file-until-collection-adapter-exists]]
