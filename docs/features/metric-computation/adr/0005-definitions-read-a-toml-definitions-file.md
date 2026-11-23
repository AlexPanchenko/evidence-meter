---
status: Accepted
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
---

# F1 ADR 0005 — Read a TOML definitions file with tomllib

- **Status:** Accepted
- **Date:** 2026-11-23
- **Deciders:** capstone owner, with Claude during the sad-builder walk
- **Owning context:** definitions
- **Gate:** I ✗ M ✗ A ✓ D ✓ → 2/4

## Context

F1 is the first feature to read the private definitions file: definition versions (formula id, inputs,
minimum data, published or retired) and one state map per team (PRD AC-04, AC-05, AC-10; CONTEXT "State
map"). Its contents stay outside git; only Definitions reads it (AGENTS.md, bc-map). SAD §5 needs its format
and location.

## Decision drivers

- Standard library first; F1 adds no dependency (AGENTS.md, SAD §2).
- A Lead edits the state map by hand after an `unmapped_states` refusal (PRD AC-04).

## Considered options

1. **TOML read with `tomllib`** — path from `EVIDENCE_METER_DEFINITIONS`, default
   `~/.config/evidence-meter/definitions.toml`.
2. **JSON read with `json`** — same location, `.json`.

## Decision outcome

**Chosen:** TOML. Both are standard library; TOML allows comments, so a Lead can note why a tracker state
maps where it does, and is easier to edit by hand.

## Consequences

**Positive**
- No dependency; tests write a synthetic TOML file to a temp directory.

**Negative**
- `tomllib` only reads; nothing in the tool writes the file (by design: Definitions never writes it).
- A malformed file stops the command with a clear message; it is a usage error, not a PRD refusal code.

**Neutral**
- A missing file is the refusal `definitions_missing` (PRD AC-05).

**Stored data**
- The file is the stored format of definitions and state maps. The version and state map are hashed from
  their parsed, canonical form (F1 ADR 0008), so reformatting the file does not change a hash; changing a
  mapping does.

## Links

- PRD: [[../PRD.md]] AC-04, AC-05, AC-10
- SAD: [[../sad.md]] §5, §8
- Related ADR: [[0008-computation-key-measurements-by-every-input]]
