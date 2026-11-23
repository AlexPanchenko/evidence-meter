---
name: brief-builder
description: Turn a raw idea for an internal engineering tool or a feature of one into a confirmed idea brief (17 sections, at most 5 pages) through a Socratic interview, verified competitor research, three strategic approaches, a three-lens review, a clean-context devil's advocate, and Claude-proposed RICE and feasibility the owner confirms. Use when the owner says "brief for <slug>", "new idea <slug>", "interview <slug>" or "/brief-builder <slug>" in a repository whose results must stay team-level and public-safe. Writes docs/features/<slug>/idea-brief.md and, for new domain words, docs/features/<slug>/CONTEXT.md.
---

# brief-builder

A standalone variant of the SDLC plugin's `interview` skill, tuned to how this owner works: internal
engineering tools, readers who are leads and managers, a public repository, and outputs that must never
rank people. Same flow as the plugin (depth, capture, Socratic, research, approaches, review, devil's
advocate, RICE, feasibility, recommendation, write, self-check, commit); the changes are listed at the end.

## Inputs

- `<slug>`: kebab-case. Missing → suggest 2-3 from the idea and ask.
- Optional: notes, a ticket id, an existing `CONTEXT.md`.
- Optional: `--out <path>` writes the brief to another file (a comparison run); the existing brief is not
  touched and step 0's "update instead" rule does not apply.

## Hard rules

- Every checkpoint below is a real `AskUserQuestion`; never answer one for the owner, in any permission mode.
- Questions in the owner's language (English unless the owner writes in another). Each question: context
  (where we are, what is known), why it matters, what to look at. Each option: what changes in the brief,
  the plain meaning, and the hidden catch. Gloss every acronym on first use.
- Synthetic and public data only: no organisation, client, person or internal URL in the brief, the
  glossary or a sub-agent prompt. If the owner's answer contains one, ask for a generic wording.
- No value, metric or example per person. If the idea itself needs one, stop and say so.

## Protocol

### 0. Setup (read only)
Read `templates/idea-brief.md`, `CONTEXT.md` (repo root and `docs/features/<slug>/`), and
`references/repo-patterns.md`. If `docs/features/<slug>/idea-brief.md` is `Confirmed` and under two weeks
old, update it instead of starting over.

### 1. Depth (checkpoint)
`easy` (4 checkpoints, no sub-agents), `medium` (default, full flow), `hard` (full flow, a third Socratic
batch, 5+ competitors). Recorded in the frontmatter. Skip this checkpoint if the owner already named a depth.

Easy route, exactly: checkpoint 1 = raw idea + evidence of the pain + who is affected (one call);
checkpoint 2 = success signal + binding constraint; checkpoint 3 = RICE, feasibility and recommendation
in one call; checkpoint 4 = pending glossary terms (skip if none). Claude does steps 5-8 itself: one
web search (rows marked snippet only) plus the status-quo row, one paragraph per approach, a 3×3 matrix,
and the four standard failure modes from step 8. If an earlier brief for the same slug exists in this
session's context, run in a fresh session: approaches and matrix copied from memory are not a new run.

### 2. Raw idea (checkpoint)
Offer 2-3 one-to-three-sentence wordings drawn from the README or the owner's notes, each with a different
emphasis (outcome, pain, contract); the owner picks one or types their own. Kept verbatim in §1.

### 3. Socratic batches (checkpoints, 2 questions each)
Pick from these categories; offer concrete, generic options the owner can pick or replace:
- **Pain episode**: who lost what, how often; is the size measured or estimated? (estimated → §15).
- **Tried before**: spreadsheet, a vendor dashboard, nothing systematic; why it failed.
- **One success signal**: time saved per unit of work, reproducibility, or coverage; baseline → target.
- **Binding constraint**: time box, one-slice scope, a context boundary.
- **Why now** (hard): the trigger and the cost of waiting.
- **Runner and reader** (hard): who runs it, who reads it, how many units (teams, services, months).
- **Who is affected by the output** (always): could the output identify or rank a person? → §16.

### 4. Glossary capture
Every new domain word in an answer goes to a pending list. Skip generic technical words. Terms are written
in step 12 through `fix-term` (definition + NOT-boundary against the nearest homonym in this repository).

### 5. Competitor research (sub-agent `sdlc:researcher`)
5+ rows at hard depth: Product · URL · Features · Value 1-5 · Gap, a footnote per row with date and query,
and a mark **fetched** or **snippet only**. Always add a row "do nothing / keep the manual process" so the
brief compares against the status quo. No invented products; fewer real rows is fine.

### 6. Three approaches (sub-agent `sdlc:strategist`)
Simplicity, Differentiation, Balanced. For internal tools, check that the three really differ on one of:
unit of work (one team vs all teams), depth of trust (stamp vs drill-down), or build vs adopt. Each:
Name, Thesis, For whom, Outcome metric, Key trade-off, Effort S/M/L.

### 7. Three-lens review (sub-agent `sdlc:analyst`)
Engineer (abstract: surface, failure modes, testability; no product or library names), Executive, UX.
3×3 matrix, +/0/− with a six-word reason per cell.

### 8. Devil's advocate (sub-agent `sdlc:devils-advocate`, mode B, clean context)
Give it only the idea, the users and the approaches. Ask for 5-10 failure modes with the production
signal, ranked. Always ask it to cover: a believable wrong number, a per-person leak, a definition changed
without a new version, and missing data shown as zero. Top one → §10; the rest → §9.

Steps 5-6 run in parallel; 7-8 run in parallel once the approaches exist.

### 9. RICE (checkpoint, one batch of four)
Claude proposes each number with its source: Reach in **units of work per quarter** (team-months,
service-releases), not readers; Impact on 0.25/0.5/1/2/3; Confidence from the count of open questions
(three or more → 0.5); Effort in person-weeks from the approach's signal. Score the leading approach and
show the other two for comparison. Record owner changes as "owner lowered from X".

### 10. Feasibility (repo scan + checkpoint)
Scan `src/`, `migrations/`, `tests/`, `docs/features/` and git history for adjacent shipped work. Tech,
Skills, Time: ☑ / ☐ / TBD, each citing a path or a commit. A TBD stays TBD with an owner in §15.

### 11. Recommendation (checkpoint)
One approach, 3-5 sentences citing §6 (one gap), §8 (one cell), §11 (RICE), §12 (feasibility). Options:
accept, pick another, TBD (blocks the PRD).

### 12. Write
Apply pending glossary terms (one checkpoint per term). Create `docs/features/<slug>/idea-brief.md` from
the template; fill all 17 sections; frontmatter `status: Confirmed`, RICE and feasibility `confirmed`,
dates. The two parked approaches go to §14 with a revisit trigger.

### 13. Self-check (commands, show the output)
- `grep -c '^## '` → 19 (17 sections + Related + DoD).
- Banned in the body: the repository's own stack names from `references/repo-patterns.md` plus datastore,
  broker and library names; `p95`/`p99`; endpoints.
- No organisation names or identifiers: grep against the repo's denylist if one exists; otherwise read §2-§4.
- `wc -w` ≤ 2400.
- §13 cites §6, §8, §11 and §12.
Fix and re-run until clean.

### 14. Commit and hand-off
Run the repository's proving command, then propose the commit (the repository's subject convention first,
e.g. `[lesson-id] 01: idea-brief for <slug>`). Next: `write-prd <slug>` or the owner's own PRD skill.

## Definition of done
- Brief and glossary exist; every checkpoint was answered by the owner.
- 17 sections, no banned terms, ≤ 2400 words, §13 cites four sections, §16 answers the per-person question.
- Every competitor row is marked fetched or snippet; a status-quo row exists.

## What changed from the plugin's interview skill (and why)
- English, owner-language questions; offered wordings for the raw idea → faster capture, same verbatim rule.
- Plugin agents (`researcher`, `strategist`, `analyst`, `devils-advocate`) instead of ad-hoc prompts → the same
  persona every run.
- New §16 Data and people and §17 Evidence of the pain → the two risks that matter for metrics tools:
  ranking people, and acting on an unmeasured pain.
- Status-quo row and fetched/snippet marks in §6 → research honesty is visible.
- Reach in units of work, owner adjustments recorded → RICE that internal tools can use.
- Devil's advocate always covers four standard failure modes → the known risks of a metrics tool are never skipped.
