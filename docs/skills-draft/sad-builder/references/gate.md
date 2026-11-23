# Blast-radius gate: 4 criteria

Score every decision, show the score next to it in the section render, and write an ADR when **2 of 4**
fire. 1 of 4 stays inline, except in §4, where it is asked as borderline. 0 of 4 is inline.

Render: `I ✓ M ✓ A ✗ D ✓ → 3/4, ADR`.

## I — Irreversible

Would choosing differently in three months take **≥ 3 days** of rework (code, data, tests, docs)?

- Fires: integration style between contexts; identity of stored records; where person data is dropped;
  surface choice that brings sign-in.
- Does not fire: a library inside one module; a config value; a name an IDE renames.

## M — Multi-module

Does the decision change a contract seen by **≥ 2 contexts** (or a context and `entrypoints`)?

- Fires: an event type in `shared/`; a refusal code list used by several contexts; a table-naming rule all
  repos follow; a type passed through `entrypoints/`.
- Does not fire: a private function or a table only one context's repo reads.

## A — Real alternative

Would a reader in six months ask "why not X?" where X is serious, not excluded by §2 or AGENTS.md?

- Fires: two reasonable engineers would pick differently (UTC vs team-local months; typed results vs
  exceptions).
- Does not fire: X needs a dependency §2 rules out without the owner's OK (YAML parser), or contradicts
  the dependency rule (a context reading another's tables). Such X is a strawman; never list it in an ADR.

## D — Stored data (added in this skill)

Does the decision change **what is stored or what stored data means**: a table, a key, a column's
meaning, a stored format, the canonical form a hash is computed over, the timezone of stored timestamps?

Why it is a criterion here: in this repository a stored-data change means a SQL migration pair, a
re-check of golden data, and possibly a different hash for every existing snapshot, so it is costly even
when it touches one context and has no rival option. In the first SAD (metric-computation), 6 of 8 ADRs
changed stored data.

- Fires: measurement key; dropping person fields at import; table prefixes; UTC normalisation.
- Does not fire: CLI wording; which function computes a median; log format to stderr.

## Targets

ADR count for an M feature: 5-12. Below 5, look for a missed D or I. Above 12, bundle: one ADR per
decision, not per consequence.

## Self-review before the critic

- Every ADR still scores ≥ 2/4 when re-scored cold.
- No inline decision scores ≥ 2/4 (promote it).
- No ADR lists a strawman option.
