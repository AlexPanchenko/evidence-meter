---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0002 — Deliver F1 as a CLI only and keep the API health-only

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

PRD §8 asked whether F1 offers the value through the local API. Repo ADR 0004 defers OIDC sign-in to the first feature that serves data, so an API read endpoint would pull sign-in into F1. The target surface is the first §4 decision; every later stage (api-forge, break-tasks, plan-tests) reads it from the SAD frontmatter.

## Decision drivers

- Delivery window: design in week 1, build in week 2, one developer (sad.md §2).
- Team-level only: every extra output path is another place a per-person value could leak (sad.md §1 QG-2).
- Repo ADR 0004: serving data brings sign-in.

## Considered options

1. **CLI only** — `target_surfaces: [cli]`; the API keeps `/health` only.
2. **CLI and a local API read endpoint** — `target_surfaces: [cli, backend-service]`; brings OIDC sign-in into F1 per repo ADR 0004.

## Decision outcome

**Chosen:** Option 1. The Lead is the only F1 user and works in a terminal; sign-in belongs to the first feature that needs a browser (Reporting's review page). The gate scored 1 of 3 (a real alternative), recorded as an ADR because it closes a PRD open question and interacts with repo ADR 0004.

## Consequences

**Positive**
- F1 stays size M with no authentication work.
- One output path to test for per-person fields.

**Negative**
- Engineering managers see nothing until Reporting ships.
- A second surface later needs its own contract (OpenAPI) and sign-in.

**Neutral**
- Adding an API later is additive: the compute use case is surface-independent (ADR 0003).

## Links

- PRD: [[../PRD.md]] §8 (open question 2), §6.1 (abuse case: serving the value to other machines)
- SAD: [[../sad.md]] §4
- Related ADR: repo [0004 auth deferred](../../../adr/0004-auth-oidc-deferred.md); [[0003-orchestrate-compute-in-entrypoints-with-in-process-events]]
