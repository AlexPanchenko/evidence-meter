---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0007 — Return refusals as typed results with stable codes

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

F1 has seven ways a run stops with a reason: definitions file missing (AC-05), version retired (AC-10), snapshot missing (AC-07), unmapped states (AC-04), period not closed (AC-06), person breakdown (AC-09) and a re-run that differs (AC-03). They arise in Definitions, Collection, Computation and the CLI. bc-map treats a refusal as a result, not an error, and the API envelope already uses `{"error": {"code", "message"}}`.

## Decision drivers

- Honest refusal, all-or-nothing: a plain reason and nothing recorded (PRD §6 NFR, sad.md §1 QG-3).
- Tests must assert on a stable code, not on message text (PRD §5 error ACs).
- The future API envelope should reuse the same codes (architecture-map, Error handling).

## Considered options

1. **Typed results with stable codes** — A `Refusal(code, message, details)` value in `shared/` with a closed list of snake_case codes; each context returns it instead of raising; the CLI prints the message and exits non-zero with the code's exit status.
2. **Exceptions per refusal** — A `RefusalError` hierarchy raised where the refusal arises and caught once in the CLI.

## Decision outcome

**Chosen:** Option 1. Refusals show in function signatures, so a caller cannot forget one; tests assert on codes; and Evidence Guard's Verdict (a later feature) follows the same result style. The codes: `definitions_missing`, `version_retired`, `snapshot_missing`, `unmapped_states`, `period_not_closed`, `person_breakdown`, `rerun_differs`.

## Consequences

**Positive**
- One closed list of codes shared by the CLI now and the API envelope later.
- Refusal tests are exact and independent of wording.

**Negative**
- More plumbing: every call site handles a result union.
- Adding a code is a contract change for the CLI exit statuses (documented by api-forge).

**Neutral**
- Unexpected failures (a corrupt database, a bug) stay exceptions; only domain refusals are results.

## Links

- PRD: [[../PRD.md]] §5 AC-03..AC-07, AC-09, AC-10
- SAD: [[../sad.md]] §8 (error and refusal model), §6 flow 2
- Related ADR: [[0003-orchestrate-compute-in-entrypoints-with-in-process-events]]
