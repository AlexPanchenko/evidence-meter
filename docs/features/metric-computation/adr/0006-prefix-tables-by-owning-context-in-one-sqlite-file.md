---
status: Accepted
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# 0006 — Prefix tables by owning context in one SQLite file

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner (Architect), with Claude during the architecture-design walk

## Context

F1 adds the first real tables: Collection's snapshots and Computation's measurements. The repo rule is that each context owns its tables behind its own repo layer and never reads another's (architecture-map, Persistence). The scaffold has one SQLite file from `EVIDENCE_METER_DB` and one migration runner (repo ADR 0003). The choice fixes how ownership shows in storage for every later context.

## Decision drivers

- Dependency rule and context ownership (sad.md §2, §5).
- All-or-nothing writes: a compute run writes only Computation's tables in one transaction (PRD §6 NFR, sad.md §1 QG-3).
- One developer: one migrate, one backup, one config value (sad.md §2).

## Considered options

1. **One file, tables prefixed by owner** — `collection_*`, `computation_*`, later `definitions_*`, `evidence_guard_*`, `reporting_*` in the one SQLite file; a test asserts each context's SQL names only its own prefix.
2. **One SQLite file per context** — A database file and a migrations folder per context; the runner and `make migrate` handle several databases.

## Decision outcome

**Chosen:** Option 1. It keeps the existing runner and config unchanged and makes ownership visible in every statement; the prefix test turns the convention into a check, like the dependency-rule test does for imports.

## Consequences

**Positive**
- No change to `platform/migrate.py`, `make migrate` or config.
- Ownership is checkable by a test over the SQL in each context's repo layer.

**Negative**
- Isolation is a convention plus a test, not a physical wall; a careless join is possible until the test catches it.

**Neutral**
- Splitting into per-context files later is a data copy per prefix, made easier by the prefixes themselves.

## Links

- PRD: [[../PRD.md]] §6 (all-or-nothing)
- SAD: [[../sad.md]] §5
- Related ADR: [[0003-orchestrate-compute-in-entrypoints-with-in-process-events]]; repo [0003 persistence on SQLite](../../../adr/0003-persistence-sqlite.md)
