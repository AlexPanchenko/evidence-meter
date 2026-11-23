---
status: Confirmed
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: M     # set by sdlc:classify-size 2026-11-23
stage: "01"
depth: hard
ticket: "none (capstone F1)"
value_score:
  rice: 7.5
  state: confirmed
  confirmed_at: "2026-11-23"
feasibility_state: confirmed
---

<!-- Stage 01 → produced by /sdlc:interview metric-computation (depth hard), 2026-11-23 -->

# Idea Brief — metric-computation (F1)

## 1. Raw idea
Given a closed month's snapshot for one team, compute the first metric from a versioned definition, so
every number names the definition version and the inputs it came from, and nobody argues about how it was
counted.

## 2. Problem
Collecting and computing engineering metrics by hand from the written guide takes a lead several hours per
team per month, so it is done late or skipped. Nothing systematic has been tried: values are computed ad hoc
when someone asks. The hours figure is the owner's estimate; no baseline was measured (§15).

## 3. Users
- **Lead** (runs it): delivery or team leads, monthly, for the teams they own; roughly 5-15 teams in total.
- **Engineering manager** (reads it): reads the team values on the reviewed monthly page.
- Results are about teams only; no person is a subject of the output (CONTEXT.md, invariants).

## 4. Why now
The metrics guide has just been written; without a tool it will be applied inconsistently from the first
month, and the first months set the baseline everyone compares against. The capstone also gives a fixed
delivery window this month: one person, part-time, about one week from spec to working code.

## 5. Out of scope
- A second metric: F1 is exactly one metric end to end; the next one is F2.
- Running all teams in one go (approach C, parked) and drill-down to records (approach B, parked).
- Reading the live tracker or Git: collection is a separate context; F1 reads a stored snapshot.
- Deciding whether a value may be shown: that is Evidence Guard's job, after F1.
- Any value, column or log line per person.

## 6. Competitive analysis
| # | Product · URL | Features | Value per feature (1-5) | Gap |
|---|---|---|---|---|
| 1 | Apache DevLake · https://devlake.apache.org/docs/DORA | Project-level delivery metrics; scope config of what counts; editable dashboard queries; tracker + Git | 4 | No definition versioning or thin-data handling described; values do not cite a definition version; a data stack to run, not a closed-month run |
| 2 | Cortex Eng Intelligence · https://docs.cortex.io/eng-intelligence/jira-metrics | Custom metrics; team and service segmentation; drill-down to data | 3 | Versioning and low-data handling not mentioned; per-person availability not stated; live dashboard |
| 3 | CloudBees flow metrics · https://docs.cloudbees.com/docs/cloudbees-platform/latest/analytics/flow-metrics | Five flow metrics; admin maps issue types to categories | 3 | Mapping is configuration, not a versioned written definition; traceability and refusal not verified |
| 4 | LinearB custom PM metrics · https://linearb.io/blog/custom-pm-metrics | Git + project data; custom tracker metrics | 3 | Search snippet only; versioning, traceability, refusal unverified |
| 5 | Tracker built-in development metrics · https://support.atlassian.com/jira-software-cloud/docs/key-metrics-on-the-development-page/ | Fixed built-in pull-request metrics | 2 | Search snippet only; fixed metrics, no user definitions or versions |

Footnotes (all 2026-11-23): row 1, query "open source DORA metrics tool engineering metrics Git issue tracker
dashboard", page fetched; row 2, query "engineering intelligence platform flow metrics custom metric
definitions Jira Git", page fetched; rows 3-5, same query, snippets only. Also seen, not assessed: Middleware,
OpenDORA, Four Keys. Silence on versioning in a page is not proof the product lacks it.

**Gap that matters:** none of the products checked pairs a written, versioned definition with a value that
names that version and its inputs.

## 7. Strategic approaches

### Approach A — One Team, One Number
- **Thesis**: a lead names a team and a closed month and gets the one F1 metric stamped with definition id, definition version and the input values it used; no setup, no extras.
- **For whom**: a lead running the first baseline month for a pilot team.
- **Outcome metric**: a person's time to produce the first metric for one team-month: hours by hand → under 5 minutes.
- **Key trade-off**: one run per team (5-15 a month); no look behind the stated input values.
- **Effort signal**: S
- **Recommended?** ●

### Approach B — Every Number Explains Itself
- **Thesis**: every measurement traces from value to inputs to the team-level snapshot records behind each input, and can be recomputed under any definition version side by side.
- **For whom**: engineering managers who must trust or challenge a number without asking the lead.
- **Outcome metric**: TBD — needs a baseline count of "how was this counted?" questions at the first review.
- **Key trade-off**: misses this month's window; must decide which records may be shown without identifying a person.
- **Effort signal**: L
- **Recommended?** ◯

### Approach C — Whole Portfolio, Reproducible Month
- **Thesis**: one run computes the F1 metric for every team in a closed month, each with its version and inputs, and a re-run on the same snapshot gives the identical number.
- **For whom**: leads who own 5-15 teams and want the month done in one sitting.
- **Outcome metric**: a person's time for one closed month across all their teams: hours × teams → under 5 minutes.
- **Key trade-off**: no drill-down to records; all-teams handling pushes past the one-week window.
- **Effort signal**: M
- **Recommended?** ◯

## 8. Multi-perspective feedback

### Engineer
- A: smallest surface — one pure formula, one snapshot read, one stamp; golden data covers it; one failure mode (missing or incomplete snapshot).
- B: largest surface — record lineage, recompute under any version, and a filter for showable records, which adds a person-leak failure mode that is hard to test fully.
- C: A's formula over many teams; new work is partial failure and identical re-runs; "re-run gives the same number" is a free regression test.
- Volume is negligible at 5-15 teams a month for A and C; B's lineage grows with records.

### Executive
- A fits the one-week budget and proves the core promise (every number names its version and inputs); the lead still repeats it per team.
- C matches the real unit of work (the whole month) and the time target most directly, but is over budget.
- B is the long-term trust moat, but misses the window and has no outcome metric yet.
- B's privacy decision is a policy question that would stall a solo, part-time build.

### UX-researcher
- A: easy to learn (team + month → number), tedious when repeated; trust rests on the version stamp.
- C: one action a month, least friction; partial failure is not yet described.
- B: most trust for readers, heavier first use; withheld records may feel like dead ends.

### Synthesis matrix
|         | Engineer | Executive | UX |
|---------|:--------:|:---------:|:--:|
| App. A  | + small, pure, golden-testable | + ships in week, proves promise | 0 simple but repeated per team |
| App. B  | − lineage plus person-leak risk | − misses window, outcome undefined | + traceable numbers build trust |
| App. C  | 0 batch failures; determinism testable | 0 right scope, over budget | + one run per month |

## 9. Trade-offs and edge cases

### Trade-offs per approach
| Approach | Pros | Cons |
|---|---|---|
| A | Smallest, testable, fits the window, proves traceability | Repeated per team; no drill-down; trust rests on the stamp |
| B | Highest trust, explains definition changes | Size L, person-leak risk, no outcome metric |
| C | One run a month, reproducibility as a test | Partial-failure handling, over the window |

### Edge cases
- Teams use the tracker differently (done states, won't-do, duplicates, sub-tasks): one definition maps them alike.
- A team of one or two people: a team value is really one person's value.
- A definition changed in place without a new version number.
- Work reopened or backdated after the month closed; time-zone edges at the month boundary.
- A broken feed or a team without a repository appears as zero instead of "no data".
- A version is published or retired between two teams' runs, so one page mixes versions.
- Per-team setup outweighs the time saved.

## 10. Risks
- **Top (devil's advocate): a believable wrong number.** Tracker usage differs by team; the value carries a version and inputs, so it looks verified while it is wrong. Nothing errors; the signal is a manager's own count disagreeing and leads going back to manual counting.
- A per-person leak through a tiny team or recorded inputs that keep assignees; a public copy cannot be recalled.
- A version label that lies because the private definition was edited in place.
- Zero shown for missing data.
- Mixed definition versions on one page.

## 11. RICE — Claude proposed, owner adjusted
- **Reach (R)**: 15 team-months per quarter — §3 Users, pilot of about 5 teams × 3 months (owner lowered from 30).
- **Impact (I)**: 1 — §2 Problem: hours per team-month, but one metric removes only part of the manual work; §8 Executive: proves the core promise (owner lowered from 2).
- **Confidence (C)**: 0.5 — three open questions in §15: unmeasured baseline, first metric not chosen, top risk not mitigated.
- **Effort (E)**: 1 person-week — §7 approach A, signal S; a dedicated week (owner lowered from 1.5).
- **RICE = R × I × C / E = 15 × 1 × 0.5 / 1 = 7.5** (C: 1.9 with E = 4; B: 0.9 with E = 8)
- **State**: confirmed

## 12. Feasibility — Claude proposed, owner confirmed
- [TBD] **Tech**: the computation context is an empty skeleton; no snapshot, definition or formula code exists, and Collection is not built yet. How F1 gets its snapshot is decided in the SAD (§15).
- [☑] **Skills**: the scaffold, migration runner, dependency-rule test and context rules were built with the same language and toolchain (S5, 2026-11-22).
- [☑] **Time**: the S5 scaffold shipped in one day; F1 spec work is in week 1 and code in week 2.
- **State**: confirmed (Tech left TBD by the owner)

## 13. Recommendation
**Selected: Approach A — One Team, One Number.** It scores RICE 7.5 against 1.9 for C and 0.9 for B (§11),
and it is the only approach that fits the one-week window. Feasibility has Skills and Time confirmed and
Tech open until the snapshot source is decided (§12), so the recommendation carries that warning. The
engineer view rates it "+ small, pure, golden-testable" and the executive view "+ ships in week, proves
promise" (§8). It delivers the gap none of the five checked products covers: a value that names its
definition version and inputs (§6). The core is built so that looping over all teams (C) is cheap next.

**Locked-in pointer**: the PRD covers one metric for one team and one closed month, with the result stamped
with definition id, version and inputs; the top risk (§10) needs an acceptance criterion on per-team tracker
differences or an explicit non-goal.

## 14. Parked & rejected approaches
| # | Approach | Status | Reason | Revisit trigger |
|---|---|:---:|---|---|
| B | Every Number Explains Itself | parked | Size L, person-leak risk, no outcome metric | Managers question values at the first monthly reviews |
| C | Whole Portfolio, Reproducible Month | parked | Over the one-week window; partial-failure handling | A is in use and leads run it for 5+ teams a month |

## 15. Open questions
- [ ] Which metric is first? — owner: capstone owner, due: 2026-11-24 (before the PRD)
- [ ] Measure the by-hand baseline for one team-month — owner: capstone owner, due: 2026-11-30
- [ ] How does F1 get a snapshot before Collection exists (fixture or minimal collection)? — owner: capstone owner, due: S7 (SAD)
- [ ] How are per-team tracker differences (done states, won't-do, sub-tasks) handled? — owner: capstone owner, due: PRD
- [ ] Minimum team size before a value is a team value — owner: capstone owner, due: Evidence Guard feature

## Related
- [CONTEXT.md](CONTEXT.md) — glossary (DefinitionVersion, Formula, Input, Lead, Measurement, Period)
- [SPEC.md](../../../SPEC.md) — v1 goals 2 and 3, acceptance criterion 2
- [docs/bc-map.md](../../bc-map.md) — Computation context and its events

## DoD self-check
- [x] 15 sections present
- [x] No anti-pattern terms (datastore, broker, library names)
- [x] Length ≤ 5 pages (~2200 words)
- [x] Frontmatter status: Confirmed
- [x] RICE confirmed (state: confirmed)
- [x] Feasibility confirmed (state: confirmed; Tech TBD by the owner)
- [x] Recommendation present with rationale citing 4 upstream sections (§6, §8, §11, §12)
