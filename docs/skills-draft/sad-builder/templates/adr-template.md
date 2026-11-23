---
status: Accepted
owner: "<decision owner>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: M
stage: "04-05"
ticket: "<ticket or 'none'>"
---

<!-- File name: NNNN-<context>-<decision-in-imperative-kebab>.md, numbered per feature.            -->
<!-- <context>: collection | definitions | computation | evidence-guard | reporting | shared |       -->
<!--            entrypoints | platform | web — the part that changes most; 'shared' if several.     -->
<!-- ✓ 0004-computation-key-measurements-by-natural-key.md   ✗ 0004-reproducibility.md (a problem)   -->
<!-- In prose: "F<n> ADR NNNN" for feature ADRs, "repo ADR NNNN" for docs/adr/.                      -->

# F<n> ADR NNNN — <decision in imperative form>

- **Status:** Accepted
- **Date:** <YYYY-MM-DD>
- **Deciders:** <owner>, with Claude during the sad-builder walk
- **Owning context:** <context>
- **Gate:** I <✓/✗> M <✓/✗> A <✓/✗> D <✓/✗> → <n>/4

## Context

<2-4 sentences: what is happening and why it must be decided now; cite the SAD section and the PRD item
that raised it.>

## Decision drivers

<Only from PRD §6 NFR, SAD §1 quality goals, SAD §2 constraints or AGENTS.md. No drivers from taste.>

- <driver> (<source>)

## Considered options

<Every option the owner saw, including rejected ones. No strawman: nothing §2 or AGENTS.md excludes.>

1. **<Option>** — <one sentence>.
2. **<Option>** — <one sentence>.

## Decision outcome

**Chosen:** <option>. <1-2 sentences: why, against the drivers.>

## Consequences

**Positive**
- <…>

**Negative**
- <…>

**Neutral**
- <…>

**Stored data** (fill when D fired)
- <tables, keys, formats or meanings this fixes; the migration or golden-data impact of changing it later>

## Links

- PRD: [[../PRD.md]] §<n> (<AC / NFR / open question>)
- SAD: [[../sad.md]] §<n>
- Related ADR: <[[NNNN-<context>-<decision>]] or repo ADR NNNN>
