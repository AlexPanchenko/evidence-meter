---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0009 — Record "no finished passes" as an outcome, never as zero

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** computation
- **Gate:** I ✗ M ✓ A ✓ D ✓ → 3/4

## Context

AC-01b: when a team finished no passes in the period, the system records a measurement that says so, shows
no number and no zero, and names the definition and inputs. It is a formula result, not a refusal (PRD §1
critic note). Evidence Guard will later read it through `MetricComputed`.

## Decision drivers

- Never a misleading number or a zero (PRD §2 goal 3, CONTEXT "Measurement").
- All-or-nothing holds because AC-01b is a result, not a refusal (PRD §1).

## Considered options

1. **Outcome column plus NULL value** — `outcome` is `value` or `no_finished_passes`; `value` is NULL only
   with the second; `MetricComputed` carries the same pair.
2. **NULL value alone** — a NULL value means no finished passes.

## Decision outcome

**Chosen:** outcome column. A second reason for "no value" (F2 metrics) becomes a new outcome, not a second
meaning of NULL; Evidence Guard reads the reason, not a convention.

## Consequences

**Positive**
- The terminal reply and the event say why there is no value in words.

**Negative**
- Two columns must agree; the migration adds a CHECK constraint.

**Neutral**
- The AC-03 match and defect rules compare outcome and value together.

**Stored data**
- `computation_measurements.outcome` (closed list) and nullable `value`; adding an outcome later is a
  migration of the CHECK constraint.

## Links

- PRD: [[../PRD.md]] AC-01b, §2
- SAD: [[../sad.md]] §6 flow 1, §8
- Related ADR: [[0008-computation-key-measurements-by-every-input]]
