---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0001 — Serve F1 through the CLI only

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** entrypoints
- **Gate:** I ✓ M ✓ A ✓ D ✗ → 3/4

## Context

PRD §8 left open whether F1 offers the value through the local API. Serving data from the API makes a
feature the first data-serving one, which brings OIDC sign-in (repo ADR 0004) and the API error-envelope
gap named in the architecture map. SAD §4 opens with this surface choice.

## Decision drivers

- Team-level only and person data in the snapshot: a narrower surface is a smaller leak surface (PRD §6.1).
- Size M and the capstone delivery window (PRD §1, `.size`).
- No server reachable beyond localhost before sign-in exists (SPEC non-goals, repo ADR 0004).

## Considered options

1. **CLI only** — `import` and `compute` commands in `entrypoints/cli.py`; no route.
2. **CLI and a read route in the API** — the same result as JSON under `/api`, with OIDC sign-in.

## Decision outcome

**Chosen:** CLI only. It meets every PRD acceptance criterion; the API adds sign-in and the envelope fix,
which push F1 past size M without serving a user need the PRD names.

## Consequences

**Positive**
- No auth code in F1; every output to check for person fields is the terminal and SQLite.

**Negative**
- SPEC goal 5 (same results through CLI, API and web) waits for a later feature, which then carries sign-in.

**Neutral**
- The context handlers return plain results, so an API route later wraps them without changing a context.

## Links

- PRD: [[../../PRD.md]] §8 (open question 2), §6.1
- SAD: [[../sad.md]] §4, §7
- Related ADR: repo ADR 0004; [[0002-entrypoints-orchestrate-a-run-with-shared-types]]
