---
name: sad-builder
description: Turn an approved PRD into a reviewed Software Architecture Document (Arc42 12 sections, C4 Context in §3 and Container in §5) plus context-prefixed ADRs, through a per-section Socratic walk with a 4-criterion blast-radius gate (irreversible, multi-module, real alternative, stored data), repo-specific consistency checks and a clean-context critic. Use when the owner says "SAD for <slug>", "architecture for <slug>" or "/sad-builder <slug>" in a modular-monolith repository whose results must stay team-level and public-safe. Needs docs/features/<slug>/PRD.md and CONTEXT.md; writes docs/features/<slug>/sad.md and adr/, or another folder with --out-dir.
---

# sad-builder

A standalone variant of the SDLC plugin's `architecture-design` skill, tuned to this repository: a modular
monolith of five contexts wired only in `entrypoints/`, a metrics tool that refuses values instead of
showing wrong ones, SQLite with plain SQL migrations, and outputs that must never rank people. Same flow as
the plugin (gate and depth, read upstream, read the map, bootstrap, draft, Socratic walk with gate, critic,
finalize); the changes are listed at the end. It reads no file from the plugin.

## Inputs

- `<slug>`: kebab-case. Required: `docs/features/<slug>/PRD.md` and `docs/features/<slug>/CONTEXT.md`.
  Missing → stop and name the skill that makes it (`prd-builder` or the plugin's `write-prd`; `fix-term`).
- Optional: `docs/features/<slug>/.size` (absent → M, said loudly in the handoff); `--depth easy|medium|hard`;
  `--out-dir <dir>` writes `<dir>/sad.md` and `<dir>/adr/` (a comparison run) and leaves an existing SAD and
  ADRs untouched; `--commits section|final` (default `section`; `final` when `--out-dir` is given).

## Hard rules

- Every checkpoint is a real `AskUserQuestion`; never answer one for the owner, in any permission mode.
- Questions in the owner's language. Each question: where we are, why it matters, what to look at. Each
  option: what changes in the SAD, the next mechanical step (which ADR, which section) and the hidden catch.
  Recommended option first. Every technical term glossed on first use.
- Synthetic and public data only (team-alpha, team-beta, 2026-10); no organisation, person, project key or
  internal URL. Private definitions are named, never quoted.
- No container, table, column, event field or log line that carries a value per person. If the PRD needs
  one, stop and say so.
- Numbers in §10 are copied verbatim from PRD §6; never invented or rounded.
- ADRs are `Accepted` (decided live with the owner). The SAD stays `status: Draft`; the owner accepts it.
- Every commit passes the repo's proving command (`make check`) and follows its commit rule (AGENTS.md).

## Protocol

### 1. Gate, size, depth (one checkpoint)
`test -f` the two inputs. Read `.size`. Ask the depth: **easy** (decide reversible calls yourself, keep an
assumptions ledger the owner vetoes in one batch per section, ask only gate-crossing decisions, diagrams
written with a one-line summary), **medium** (default: one question per real decision, trivial defaults
bundled, diagrams confirmed in prose), **hard** (every decision, trade-offs foregrounded). The gate and the
§11 owner-and-due rule apply at every depth.

### 2. Read upstream
PRD: §1 (committed approach, overrides), §2 goals, §3 non-goals, §5 ACs (outcome class of each), §6 NFR,
§6.1 security, §7 KPIs, §8 open questions (those due at this stage must be closed or kept open with an
owner), any §9-§11 the PRD has (data and people, errors and refusals, states and events). `CONTEXT.md`
glossary wins over everything else. Keep a list of PRD open questions due "at architecture" — each becomes a
decision in the section it belongs to.

### 3. Current architecture
Read `docs/architecture-map.md`. If its `reflects_commit` is behind `src/` changes, say so and offer to run
`/sdlc:map-architecture` first (do not re-scan here). Also read `docs/bc-map.md` (contexts, events, owners),
`AGENTS.md`, repo `docs/adr/` and [references/repo-patterns.md](references/repo-patterns.md) (recommended
containers, conventions, the reference SAD).

### 4. Bootstrap
Copy [templates/sad-template.md](templates/sad-template.md) to the target `sad.md`; fill the frontmatter
(`updated_at`, `ticket` from the PRD, `feature_size`, `target_surfaces: []`). Commit (if `--commits section`).
Read the template comments (the per-section contract) and [templates/adr-template.md](templates/adr-template.md).

### 5. Draft all sections in memory
For each §1-§12 draft the content and the numbered decisions it contains, from CONTEXT → PRD → map and
repo patterns → earlier decisions. Draft §5 from the **recommended containers** in repo-patterns (start
from the list, drop what the feature does not touch, never invent a new kind without a decision). Draft
§6 seed flows from the PRD ACs with the most refusal branches. Hygiene before asking: roles from the
glossary only, §2 matches the map, every Mermaid element declared before use, §10 numbers verbatim.

### 6. Socratic walk, section by section
For each section: render the whole proposed section with its numbered decisions, and next to **every**
decision its gate score `I M A D → n/4` ([references/gate.md](references/gate.md)). Ask one
`AskUserQuestion` per real decision (by depth) with the 4 actions: **Accept**, **Edit** (owner's wording,
regenerate, ask once more, second answer final), **Save as open question** (follow-up question for owner
and due; missing either → drop with a warning; row goes to §11 with severity `Open question`), **Drop**
(mandatory decision → re-ask once reframed; optional → leave out). Keep an edits log of every Edit / Drop /
Save (decision id, before, after, owner's reason verbatim); Accept is the baseline and not logged.

On each accepted decision run the gate: **2 of 4 → ADR**; 1 of 4 → inline, except in §4, where a 1/4 is
asked as borderline ("lock as ADR or keep inline?"). ADR file:
`NNNN-<context>-<decision-in-imperative-kebab>.md` (see the ADR template), numbered per feature, with the
4-tick score in its header and three Links (PRD §, SAD §, neighbouring ADR). In prose always write
"F<n> ADR NNNN" or "repo ADR NNNN", never a bare number.

§4 opens with the **target surface** (`cli`, `backend-service`, `web-frontend`, `worker`, `library-sdk`;
multi-select), written to frontmatter `target_surfaces`; §5 then draws one container per surface. A UI
surface gets a UI-architecture decision that reuses the map's §Frontend. A data-serving surface checks
repo ADR 0004 (sign-in) in the same question.

§3 and §5 diagrams: write the block, run `python3 -I scripts/lint_mermaid.py <sad.md>` (structural lint;
use `mmdc` too if it runs), describe the picture in prose, confirm by prose — never paste raw Mermaid as
the question. Then write the section and its ADRs, commit `sad §N: <summary>` (if `--commits section`),
and move on. Never return to a written section; drift is the critic's job.

### 7. Repo consistency checks (before the critic)
Run [references/repo-patterns.md](references/repo-patterns.md) §Checks and fix in memory what they find,
asking the owner where a fix changes a decision:
1. **Inputs complete**: every input that can change a stored value is in its identity or recorded with it.
2. **Refusal coverage**: every PRD error AC maps to exactly one refusal code in §8, and every code to an AC.
3. **Event ledger**: every bc-map event the touched contexts publish or consume is either produced in this
   design or listed in §11 accepted debt.
4. **Privacy ledger**: every place person data or private names could be stored is named in §8 (file,
   table, log, output) with "never" or the control that keeps it out.
5. **Diagram honesty**: every `alt` branch in §6 ends with its own reply to the actor; for each lint
   warning about a reply after the last `end`, check it holds for every branch or move it inside them.

### 8. Critic and finalize
Dispatch one clean-context critic (`sdlc:critic` if installed, else `general-purpose`) with
[references/critic-prompt.md](references/critic-prompt.md), the SAD path, the edits log, the ADR list, and
the PRD / CONTEXT / adr paths (paths only). Resolve each finding with the owner (≤2 batches of ≤4
questions): accept the fix, other wording, or override (a §1 "Decision override" bullet with the reason).
Run the backstop scans: Mermaid lint on every block, ADR filenames `NNNN-<context>-<kebab>.md` with Status
Accepted, §9 rows ↔ `adr/` files, no `<placeholder>` left outside naming patterns. Commit the finalization
(the repo's subject rule; a lesson may name it). Print the handoff: what was decided (one line per ADR),
checks run with results, what was not verified (renders), and the next stage
(`/sdlc:complete-sequence-diagrams <slug>`).

## Changes from the plugin's architecture-design

- **Gate**: a 4th criterion, **D — changes stored data or its meaning** (a table, key, column meaning,
  stored format, canonical form); ADR at 2 of 4; the score is shown next to every decision, not only on
  accepted ones.
- **ADR naming**: `NNNN-<context>-<decision>.md` with the owning context; "F<n> ADR" vs "repo ADR" in prose,
  because the repo has its own `docs/adr/` with the same numbers.
- **§5 from recommended containers** (repo-patterns): CLI, API, web, the five context packages, SQLite,
  the private definitions file, tracker / Git / snapshot file, instead of a blank template.
- **Template sections added**: §5 "Context touch list" (contexts, tables, events changed — AGENTS.md asks
  to say when a change crosses parts), §6 "Event ledger", §8 rows for refusal codes, privacy ledger, time
  and period; §7 defaults to a deliberate N/A for a CLI-only feature.
- **New step 7, repo consistency checks**: the five checks above, each from a gap the plugin's critic had to
  catch on the first SAD (state map missing from the reproducibility key, a refusal code with no AC, an
  unpublished bc-map event, private names stored in SQLite, a reply outside an `alt`).
- **Standalone**: no `_shared/` files; the 4-action machine, the critic prompt and a Mermaid lint script
  are inside the skill. Questions in the owner's language, not fixed Ukrainian.
- **Comparison runs**: `--out-dir` and `--commits final` keep an existing SAD untouched.
