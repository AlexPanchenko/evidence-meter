---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0007 — Return refusals as typed results with a closed code list

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** shared
- **Gate:** I ✓ M ✓ A ✓ D ✗ → 3/4

## Context

Six PRD acceptance criteria end in a refusal with a plain reason (AC-04, AC-05, AC-06, AC-07, AC-09,
AC-10). Refusals come from three contexts and the CLI (SAD §6 flow 2). ARCHITECTURE.md fixes this for
Evidence Guard ("a refusal is a `Verdict` with a reason, not an error"); Computation, Collection and
Definitions refuse before any value exists, so they need their own rule.

## Decision drivers

- A plain reason, never a misleading number or a zero (PRD §2 goal 3).
- All-or-nothing: 0 partial records after a refused run (PRD §6).

## Considered options

1. **Typed result** — `shared.Refusal(code, message, details)` returned by handlers, never raised; a closed
   code list, one code per PRD AC; the CLI prints it and exits with a distinct non-zero code.
2. **Exceptions** — one `RefusalError` subclass per code, raised in a context and caught in the CLI.

## Decision outcome

**Chosen:** typed result. It matches the Verdict style the repo already chose for Evidence Guard, makes every
refusal visible in a handler's signature, and keeps tracebacks for real defects only.

## Consequences

**Positive**
- A test can list the codes and check each against one AC and one §6 branch.

**Negative**
- Every handler returns a union (value or `Refusal`); callers must check it.

**Neutral**
- Codes: `person_breakdown_refused` (AC-09), `period_not_closed` (AC-06), `definitions_missing` (AC-05),
  `definition_retired` (AC-10), `snapshot_missing` (AC-07), `unmapped_states` (AC-04). The AC-03 mismatch is
  a defect, not a refusal; a malformed definitions file or bad arguments are usage errors.

## Links

- PRD: [[../../PRD.md]] §5 (AC-04..AC-07, AC-09, AC-10), §6
- SAD: [[../sad.md]] §6, §8
- Related ADR: [[0002-entrypoints-orchestrate-a-run-with-shared-types]]
