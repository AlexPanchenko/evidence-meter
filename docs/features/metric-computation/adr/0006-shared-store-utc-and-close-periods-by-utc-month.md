---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0006 — Store timestamps in UTC and close periods by the UTC calendar month

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** shared
- **Gate:** I ✓ M ✓ A ✓ D ✓ → 4/4

## Context

A Period is a closed calendar month `YYYY-MM` (CONTEXT). AC-06 refuses a period that is not closed, and
AC-08 counts each pass in the period of its own done. Both need one timezone; snapshot files may carry
offsets. SAD §6 checks closure before any I/O.

## Decision drivers

- Reproducibility: the same snapshot gives the same passes per period (PRD §6).
- All-or-nothing: the closure check runs before the first write (PRD §6, AC-06).

## Considered options

1. **UTC everywhere** — Collection normalises timestamps to UTC at import; `shared.Period` has a pure
   `is_closed(now_utc)` (the month has ended in UTC); a pass belongs to the UTC month of its done.
2. **Team-local timezone** — a timezone per team in the definitions file; months and passes in local time.

## Decision outcome

**Chosen:** UTC. One rule, no timezone input to key or hash, and a pure check the CLI runs first. A team far
from UTC is a §11 risk to revisit with real pilot data.

## Consequences

**Positive**
- Golden data needs no daylight-saving cases; the closure check takes the clock as an argument.

**Negative**
- Work done late on the last local day of a month in a team far from UTC lands in the next month.

**Neutral**
- `ReportingPeriodClosed` stays an external trigger for later features; F1 uses the calendar rule.

**Stored data**
- Every stored timestamp is UTC (ISO 8601 with `Z`), and the canonical form hashed in F1 ADR 0003 uses it.
  Switching to local time later means a migration, a re-hash of every snapshot and new golden data.

## Links

- PRD: [[../PRD.md]] AC-06, AC-08; CONTEXT "Period"
- SAD: [[../sad.md]] §6, §8
- Related ADR: [[0003-collection-import-a-snapshot-file-as-an-immutable-snapshot]]
