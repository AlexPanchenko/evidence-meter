# sdlc-audit (draft)

Inspection skill for homework m06-l01, hard level: report which of the nine module 6 artifacts a feature
has, which are missing and which are stale. The draft lives here because Claude cannot write to
`.claude/skills/`; the owner installs it:

    mkdir -p .claude/skills && cp -R docs/skills-draft/sdlc-audit .claude/skills/

## Manual inventory: metric-computation (F1), 2026-11-23

Made by hand before the skill existed. F1 is not in production: it has finished phases 1 and 2 (idea, PRD)
and nothing after, so this is an audit of a feature in flight, not of a shipped one (the homework's
"shipped last quarter" feature would have to come from work, and its names cannot enter this repository).

Phases: 1 idea, 2 PRD, 3 architecture, 4 contracts, 5 code.

| Phase | Artifact (or missing) | Container | Consequence of the gap |
|---|---|---|---|
| 1 | `idea-brief.md`, Confirmed, commit `9438a61` | repo, feature folder | none; a second variant `idea-brief.brief-builder.md` sits beside it, so a reader must know which one is canonical |
| 1 | `CONTEXT.md`, amended after the PRD critic (`e874a4d`) | repo, feature folder | none; the brief was written before the amendment, so its "Measurement" wording is older than the glossary |
| 2 | `PRD.md`, Approved (`e874a4d`) | repo, feature folder | none; again a variant `PRD.prd-builder.md` (`506c2c4`) with more ACs and error codes, not reconciled with `PRD.md` |
| 2 | Socratic edits-log and critic findings | chat session only; summarised in PRD §1 bullets and the notebook HANDOFF | the reason behind each AC change is not in the repository; a later reader sees the result, not the debate |
| 3 | `sad.md`: missing | — | no target surface chosen; PRD §8 questions due at S7 (snapshot source, local API or command line) stay open, so work cannot be split into tasks |
| 3 | feature `adr/`: missing; repo-level `docs/adr/0001-0004` exist | repo, `docs/adr/` | decisions F1 relies on (stack, persistence, sign-in deferred) are recorded, but none of F1's own (snapshot fixture, recompute rule) |
| 3 | `docs/architecture-map.md`: present, `reflects_commit cd34458` | repo, `docs/` | stale: the scaffold `5011327` and `a9ab028` changed `src/` after that commit; architecture design would read an outdated map |
| 4 | `data-model.md`: missing; repo `migrations/0001_init` has no Measurement table | repo | where a Measurement and its inputs are stored is undecided; the all-or-nothing and re-run NFRs have nothing to test against |
| 4 | `contracts/openapi.yaml`: missing, likely N/A (F1 is command-line only); `contracts/cli.md` and `events.md` would be the contract instead | — | the command's arguments, messages and exit codes and the `MetricComputed` payload are unspecified; error codes exist only in `PRD.prd-builder.md` §10 |
| 4 | `contracts/api-sync-report.md`: missing | — | no drift check between PRD, data model and contract; follows from the two rows above |
| 5 | `tasks/` and `tasks.json`: missing | — | no task breakdown; implementation cannot start through `implement-tasks` |
| 5 | code: `computation/domain`, `app`, `infra` are empty `__init__.py` | repo, `src/` | nothing is stale yet, because there is no feature code to be newer than the documents |
| — | step plan (S7 architecture, S8 tasks) | notebook `PLAN.md`, outside the repo | the order of the next phases is visible to the owner only, not to a reader of the repository |

Most critical gap: `sad.md`. It holds the two open decisions every later artifact depends on.

## Run 2026-11-23: comparison with the manual table

First run of the installed skill: 3 present (CONTEXT Living, idea-brief Confirmed, PRD Approved), 6 missing,
0 stale, plus two variant files, the architecture map 2 commits behind `src/` and 4 open questions in the PRD.

The skill found what the manual table did not: the PRD declares no `contexts`, so code staleness can never be
checked for this feature, and it counted the open questions tied to the next phase. The manual table found
what the first run missed: the brief's content is older than the glossary change (both were last committed
together, so plain commit dates hid it), the PRD variant carries content the canonical PRD lacks (§10 error
codes), repo `migrations/` has no Measurement table, and the edits-log and the step plan live outside the
repository. The most critical artifact is `sad.md`: two PRD questions due at S7 wait on it and every later
artifact reads it; the longest-standing gap is the architecture map, out of date since the scaffold
(`5011327`, 2026-11-22). Added to SKILL.md after the comparison: content-only staleness (frontmatter syncs
ignored), `migrations/` as a stand-in, section and word counts for variants, and explicit lines for
undeclared contexts and for what the scan cannot see; the second run marks the brief stale.
