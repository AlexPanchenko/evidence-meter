---
name: prd-builder
description: Turn a confirmed idea brief into a reviewed PRD.md (8 standard sections plus §9 Data and people, §10 Errors and refusals, §11 States and events) through a short Socratic interview, a per-item walk of stories, acceptance criteria, NFRs and KPIs, and a clean-context critic. Use when the owner says "PRD for <slug>", "write the PRD for <slug>" or "/prd-builder <slug>" in a repository whose results must stay team-level and public-safe. Needs docs/features/<slug>/idea-brief.md and CONTEXT.md; writes docs/features/<slug>/PRD.md, or another file with --out.
---

# prd-builder

A standalone variant of the SDLC plugin's `write-prd` skill, tuned to this repository: a modular monolith of
five contexts that talk through events, a metrics tool that refuses values instead of showing wrong ones,
and outputs that must never rank people. Same flow as the plugin (prerequisites and depth, idea capture,
glossary, channels, draft, Socratic walk, critic, write); the changes are listed at the end.

## Inputs

- `<slug>`: kebab-case. Required: `docs/features/<slug>/idea-brief.md` (status Confirmed) and
  `docs/features/<slug>/CONTEXT.md`. Missing → stop and name the skill that makes it (`brief-builder` or the
  plugin's `interview`; `fix-term`).
- Optional: `docs/features/<slug>/.size`; `--reference <path>`; `--depth easy|medium|hard`;
  `--out <path>` writes the PRD to another file (a comparison run) and leaves an existing PRD untouched.

## Hard rules

- Every checkpoint is a real `AskUserQuestion`; never answer one for the owner, in any permission mode.
- Questions in the owner's language. Each question: where we are, why it matters, what to look at. Each
  option: what changes in the PRD and the hidden catch. Recommended option first.
- Synthetic and public data only (team-alpha, team-beta, 2026-10); no organisation, person, project key or
  internal URL. Private definitions are named, never quoted.
- No value, column or log line per person in any section. If the idea needs one, stop and say so.
- The owner sets `status: Approved` by hand; this skill writes `Draft`.

## Protocol

### 1. Prerequisites, context, depth (one checkpoint)
`test -f` the two inputs. Read `CONTEXT.md` (glossary = session state), the brief (§2-§4, §6, §10, §11, §13,
§14, §16), `.size` (if absent, classify XS-XL from PR count, time, new module/API/migration, breaking change
and confirm), `docs/architecture-map.md`, `docs/bc-map.md`, `SPEC.md` and `references/repo-patterns.md`.
Ask the depth: easy (assumptions ledger, 3-4 checkpoints), medium (default), hard (every angle).

### 2. Capture and deep-dive (checkpoints, 2-3 questions each)
Offer 2-3 one-sentence wordings of the feature from brief §13; the owner picks or types one (kept verbatim).
Then batches from: unit of work (one team and period, or all); what counts as done or excluded; repeat
behaviour (same inputs again); what the actor sees before another context has checked the value; missing
upstream data; who could be identified by the output. Every answer that changes behaviour goes into the
§1 ¶4 owner-decisions bullet.

### 3. Glossary in flow
A new domain word goes into `CONTEXT.md` at once, with a definition and a NOT-line against the nearest
homonym in `docs/bc-map.md` (one checkpoint per term). Roles and terms in §4-§5 come only from the glossary.

### 4. Channels (one multi-select checkpoint)
Reference module (pre-selected with `--reference`; suggest `platform/migrate.py`), project docs (SPEC.md
criteria, ADRs), none. Ask for exact paths; no broad scans. Record what was read in the PRD header.

### 5. Draft all 11 sections
Fill `templates/PRD-template.md`; its `<!-- Skill instruction -->` comments are the contract. Then:
- §5: ≥1 AC of each coverage type (happy, error, authorization, domain invariant, cross-context), ≥1 per US,
  each tagged with an outcome class (result / refusal / error, see repo-patterns «Refusal is a Verdict»).
- §6: start from the NFR defaults; keep N/A rows with a reason.
- §10: one row per error or refusal AC; error codes `<context>.<error_name>`.
- §11: only the transitions the feature touches; N/A is valid.
Self-scan before the walk: forbidden tokens in §5, stack words in §1-§5, a per-person field anywhere.

### 6. Socratic walk (checkpoints)
Walk §4 → §5 → §6 → §7 → §9 in batches of up to 4 items. Options per item: Approve / Edit / Drop /
Save as open question (asks owner + due at once); ACs also get «Add edge case» (adds AC-NNb). After each §5
batch re-check both floors (five coverage types, one AC per story) and the outcome-class rules:
- an error AC records nothing and has a §10 code;
- a refusal AC names an Evidence Guard reason, never a code;
- a result AC that may show no value says «shows no number and no zero».
Keep an edits-log: `{item, action, before, after, reason}` for every non-Approve answer.

### 7. Critic (sub-agent `sdlc:critic`, clean context)
Send the prompt in `references/critic-prompt.md` with the PRD path, the edits-log and the upstream paths.
Fallback only if the agent is unavailable: `general-purpose` with the same prompt. Show each finding to the
owner with Accept amendment / Different wording / Override (rationale → §1 ¶4 bullet), at most two batches.
Record the outcome as one «Critic pass: ...» bullet in §1 ¶4.

### 8. Write, self-check, commit
Write the PRD (`--out` path if given). Run and show:
- forbidden tokens in §5 only: `awk '/^## 5\./,/^## 6\./' PRD.md | grep -nE '\b(GET|POST|PUT|PATCH|DELETE)\b|(^|[ (\x60])/[a-z]|\b(200|201|400|401|403|404|409|500|503|5xx)\b|\b[a-z_]+\.[a-z_]+\b|\{[^}]*:|UNIQUE|\bFK\b|\b(INSERT|SELECT|UPDATE)\b'` → no output;
- coverage: AC count per US (none zero) and per coverage type (none zero);
- every §10 code matches `^(collection|definitions|computation|evidence_guard|reporting)\.[a-z_]+$`;
- `grep -c '^## '` → 12 (11 sections + 6.1).
Then the repository's proving command (`make check`) and propose the commit
`[<lesson-id>] 02: PRD for <slug> via prd-builder`. Next: the owner sets Approved; then architecture design.

## Definition of done

- PRD written with 11 sections (+6.1), each filled or `N/A — <reason>`; status Draft for the owner to approve.
- §5: five coverage types, one AC per story, outcome class on every AC, 0 forbidden tokens.
- §10 has a row for every error and refusal AC; codes follow the convention.
- §9 answers all five questions; no per-person output anywhere.
- Critic ran on the post-walk draft; every finding resolved or overridden with a §1 ¶4 bullet.

## What changed from the plugin's write-prd (and why)

- §9 Data and people → the per-person and small-team questions are answered in every PRD, not left to an
  abuse-case bullet.
- §10 Errors and refusals with `<context>.<error_name>` codes → error codes have a home outside the ACs, so
  §5 stays free of forbidden tokens and the API contract later has a source.
- §11 States and events from `docs/bc-map.md` → a feature that touches PageState, Verdict or a retired
  DefinitionVersion lists its transitions before architecture design.
- Outcome class (result / refusal / error) on every AC → the AC-01b drift the critic found on
  metric-computation (a recorded «no value» filed under a refusal story) is caught at draft time.
- NFR defaults for a local single-user tool → no invented availability or throughput targets; N/A rows say why.
- Self-contained: the Socratic machine and the critic prompt live in this folder; roadmap registration
  dropped (no roadmap in this repository); `--out` for comparison runs.
