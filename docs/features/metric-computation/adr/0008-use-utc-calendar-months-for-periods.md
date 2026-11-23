---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0008 — Use UTC calendar months for periods

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

A pass counts in the period of its own done (CONTEXT: Pass, Period), and a period is a closed calendar month YYYY-MM. Tracker exports carry timestamps with offsets, so a done near midnight at a month boundary can fall in different months depending on the timezone used. The rule must be fixed before golden data is written, because changing it later changes historic values.

## Decision drivers

- Reproducibility on any machine (PRD §6 NFR, sad.md §1 QG-1).
- Standard library only: zoneinfo may need the tzdata package on some systems (sad.md §2).
- AC-08: a reopened pass must land in exactly one period.

## Considered options

1. **UTC calendar months** — Collection normalises every timestamp to UTC at import; a period is the UTC calendar month.
2. **Team-local calendar months** — Each team in the definitions file names an IANA timezone; period boundaries follow it, including daylight-saving changes.

## Decision outcome

**Chosen:** Option 1. One rule with no timezone configuration, identical on every machine, and part of the canonical snapshot form (ADR 0004).

## Consequences

**Positive**
- No timezone data, daylight-saving edge cases or extra configuration.
- Canonical timestamps make the snapshot hash independent of the exporting machine.

**Negative**
- For a team far from UTC, passes done in the first or last hours of a month land in the neighbouring month compared with a local by-hand count.

**Neutral**
- Switching to team-local months later is a definition change: a new definition version, never a silent recompute. Golden data includes a pass done near midnight at a month boundary to pin the rule.

## Links

- PRD: [[../PRD.md]] §5 AC-01, AC-08
- SAD: [[../sad.md]] §8 (time and period)
- Related ADR: [[0004-identify-snapshots-by-content-hash-and-measurements-by-natural-key]]
