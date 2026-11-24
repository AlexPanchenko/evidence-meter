---
status: Confirmed
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-24"
feature_size: n/a     # product-level brief; each feature gets its own .size
stage: "01"
depth: n/a            # assembled, not interviewed (see source)
source: "assembled from SPEC.md, README.md, docs/bc-map.md and the F1 brief (docs/features/metric-computation/idea-brief.md); no new interview or research run"
ticket: "none (capstone product brief)"
value_score:
  rice: 9
  state: confirmed
  confirmed_at: "2026-11-24"
feasibility_state: confirmed
---

<!-- Stage 01, product level. Assembled 2026-11-24 from existing confirmed sources instead of a fresh
     /sdlc:interview run: the F1 interview (depth hard, 2026-11-23) already covered users, problem,
     competitors and approaches. Feature briefs live in docs/features/<slug>/idea-brief.md. -->

# Idea Brief — Evidence Meter (product)

## 1. Raw idea
Turn a written guide of engineering metrics into a tested tool: collect from an issue tracker and Git,
compute each metric from a versioned definition, refuse a value the data cannot support, and draft a
monthly page per team for a person to review and publish.

## 2. Problem
Leads compute engineering metrics by hand from the written guide. It takes several hours per team per
month, so it is done late or skipped, and two people counting the same team get different numbers because
nothing records which definition and which data a value came from. The hours figure is an estimate; a
by-hand baseline is due 2026-11-30 (§15).

## 3. Users
- **Lead** (runs it): delivery or team leads, monthly, for the teams they own; roughly 5-15 teams in total.
- **Engineering manager** (reads it): reads team values on the reviewed monthly page and compares months.
- **Definition owner** (maintains it): keeps the metric guide and its versioned definitions; changes a
  definition by publishing a new version, never by editing an old one.
- Results are about teams only; no person is a subject of any output (SPEC non-goals).

## 4. Why now
The metrics guide has just been written. Without a tool it will be applied inconsistently from the first
month, and the first months set the baseline everyone compares against. The capstone gives a fixed
delivery window: modules 7 to 11, about five weeks, one person part-time.

## 5. Out of scope
- Any output, column or log line with a value per person: the tool must not become a ranking of people.
- Organisation-specific metric codes, thresholds or identifiers in the repository; they stay in a private
  definitions file outside git.
- Hosting for several organisations, or serving beyond the local machine before sign-in exists.
- Editing tracker or Git data; the tool only reads.
- Real-time dashboards; the unit of reporting is a closed month.

## 6. Competitive analysis
| # | Product · URL | Features | Value per feature (1-5) | Gap |
|---|---|---|---|---|
| 1 | Apache DevLake · https://devlake.apache.org/docs/DORA | Delivery metrics per project; configurable scope; editable dashboard queries; tracker + Git | 4 | Values do not cite a definition version; no thin-data refusal described; a data stack to run, not a closed-month report |
| 2 | Cortex Eng Intelligence · https://docs.cortex.io/eng-intelligence/jira-metrics | Custom metrics; team and service segmentation; drill-down | 3 | Versioning and low-data handling not mentioned; live dashboard |
| 3 | CloudBees flow metrics · https://docs.cloudbees.com/docs/cloudbees-platform/latest/analytics/flow-metrics | Five flow metrics; admin maps issue types to categories | 3 | Mapping is configuration, not a versioned written definition |
| 4 | LinearB custom PM metrics · https://linearb.io/blog/custom-pm-metrics | Git + project data; custom tracker metrics | 3 | Snippet only; versioning, traceability, refusal unverified |
| 5 | Tracker built-in development metrics · https://support.atlassian.com/jira-software-cloud/docs/key-metrics-on-the-development-page/ | Fixed built-in pull-request metrics | 2 | Fixed metrics, no user definitions or versions |

Footnotes: rows reused from the F1 brief §6 (searched 2026-11-23; rows 1-2 pages fetched, rows 3-5
snippets only); not re-run for this brief. Silence on versioning in a page is not proof the product lacks it.

**Gap that matters:** none of the products checked pairs a written, versioned definition with a value that
names that version and its inputs, refuses a value on thin data, and keeps every output team-level.

## 7. Strategic approaches

### Approach A — Evidence-first monthly tool
- **Thesis**: every published number names its definition version and inputs, or is refused with a reason,
  and reaches managers only on a page a person reviewed.
- **For whom**: Leads (no counting by hand) and engineering managers (values they can trust and compare).
- **Outcome metric**: Lead time per team-month to a reviewed page: hours (estimated) → ≤ 15 minutes.
- **Key trade-off**: more built than a dashboard; value shows only after collection, computation, guard
  and reporting all exist.
- **Effort signal**: L
- **Recommended?** ●

### Approach B — Dashboard on an existing metrics platform
- **Thesis**: install an existing engineering-metrics platform and write the guide's definitions as its
  queries.
- **For whom**: engineering managers who want charts quickly.
- **Outcome metric**: teams with a live chart: 0 → all pilot teams in two weeks.
- **Key trade-off**: fast charts, but no definition versions, no refusal on thin data, and per-person
  views are built in and hard to remove.
- **Effort signal**: M
- **Recommended?** ◯

### Approach C — Spreadsheet template next to the guide
- **Thesis**: a shared spreadsheet per team-month with the guide's formulas and a version column.
- **For whom**: Leads who already count by hand.
- **Outcome metric**: Lead time per team-month: hours → about one hour.
- **Key trade-off**: cheapest, but data entry stays manual, formulas drift between copies and nothing
  stops a per-person tab.
- **Effort signal**: S
- **Recommended?** ◯

## 8. Multi-perspective feedback

### Engineer
- Pure formulas with golden data computed by hand make each metric testable in isolation.
- Five contexts wired by events keep each feature thin, at the cost of more wiring up front.
- Collection from real trackers is the least predictable part; a snapshot file import lets the core ship first.
- Platform approach B moves the work into someone else's configuration, which cannot be versioned or tested here.

### Executive
- The promise is trust: one number per team that anyone can recompute.
- A refusal with a reason is better than a believable wrong number in a management review.
- The capstone window allows one metric end to end plus the guard and page; more metrics come later.

### UX-researcher
- Leads need the reason for a refusal in plain words, or they fall back to counting by hand.
- Managers read a page, not a tool: the reviewed monthly page is the product they see.
- A per-person view, even optional, changes how teams behave towards the tool.

### Synthesis matrix
|         | Engineer | Executive | UX |
|---------|:--------:|:---------:|:--:|
| App. A  | + testable formulas, events keep slices thin | + trusted, recomputable numbers | + plain refusal reasons, reviewed page |
| App. B  | − untestable config, no versioning | 0 fast charts, weak trust story | − per-person views built in |
| App. C  | − manual entry, formulas drift | − no traceability at scale | 0 familiar but tedious to fill |

## 9. Trade-offs and edge cases

### Trade-offs per approach
| Approach | Pros | Cons |
|---|---|---|
| A | Traceable values, refusals, team-level by design, testable | Largest build; value only once the whole chain exists |
| B | Quick charts, many metrics at once | No versions or refusals; per-person views; hard to test |
| C | Cheapest, no build | Manual, drifts, no guard against per-person data |

### Edge cases
- A team with no finished work in a month: no value, never zero.
- A reopened issue: each pass counted in the month of its own done.
- Teams use the tracker differently: a per-team state map, refusal on states it does not cover.
- A definition changes mid-quarter: a new version; old values keep naming the old one.
- A team of one or two people: its team value is effectively personal (handled by Evidence Guard).
- Collection fails for one team: the page shows the refusal, not a gap or a stale number.
- No private definitions file: the tool stops with a clear message and writes nothing.

## 10. Risks
- **Top: a believable wrong number.** The value carries a version and inputs, so it looks verified while a
  team's tracker usage makes it wrong; the signal is a manager's own count disagreeing (from the F1 devil's
  advocate).
- A per-person leak through a tiny team or kept inputs; a public copy of the repository cannot be recalled.
- A version label that lies because a private definition was edited in place.
- Collection from real trackers takes longer than planned and delays the page.
- Scope: five contexts for one person in five weeks.

## 11. RICE — Claude proposed, owner confirmed
- **Reach (R)**: 45 team-months per quarter — §3 Users: up to 15 teams × 3 months.
- **Impact (I)**: 2 — §2 Problem: hours per team-month plus disagreement about numbers; §8 Executive:
  trust is the promise.
- **Confidence (C)**: 0.5 — §15 has an unmeasured baseline and no pilot data on tracker differences.
- **Effort (E)**: 5 person-weeks — §7 approach A, signal L, the modules 7 to 11 window.
- **RICE = R × I × C / E = 45 × 2 × 0.5 / 5 = 9** (B: 45 × 0.5 × 0.5 / 2 ≈ 5.6; C: 45 × 0.5 × 0.8 / 0.5 = 36,
  but C does not deliver traceability or refusal, the gap in §6)
- **State**: confirmed

## 12. Feasibility — Claude proposed, owner confirmed
- [☑] **Tech**: the modular-monolith scaffold, migration runner and dependency-rule test exist (S5); F1 has
  a full spec package (PRD, SAD with 9 ADRs, data model, CLI contract, test plan, 12 tasks).
- [☑] **Skills**: the scaffold and spec package were built with the same language and toolchain.
- [☐] **Time**: five contexts in about five part-time weeks is tight; the F1 slice (one metric, CLI) fits,
  the full chain to a published page is the risk.
- **State**: confirmed (Time left open by the owner)

## 13. Recommendation
**Selected: Approach A — Evidence-first monthly tool.** It is the only approach that closes the gap in §6:
a value that names its definition version and inputs and is refused on thin data. RICE is 9 against 5.6
for B (§11); C scores higher but drops traceability, which is the product's reason to exist. Feasibility
has Tech and Skills checked and Time open (§12), so the build goes slice by slice: F1 computes one metric
from an imported snapshot, then the guard and the page. The engineer view rates it "+ testable formulas"
and the UX view "+ plain refusal reasons" (§8).

**Locked-in pointer**: v1 is SPEC.md's goals and acceptance criteria; each feature starts from its own
brief under `docs/features/<slug>/`, first `metric-computation` (F1).

## 14. Parked & rejected approaches
| # | Approach | Status | Reason | Revisit trigger |
|---|---|:---:|---|---|
| B | Dashboard on an existing platform | rejected | No definition versions or refusals; per-person views built in | A platform adds versioned definitions and refusal |
| C | Spreadsheet template | parked | Manual, drifts, no per-person guard | The tool slips and leads need a stopgap for a month |

## 15. Open questions
- [ ] Measure the by-hand baseline for one team-month — owner: capstone owner, due: 2026-11-30
- [ ] Which tracker and Git source does Collection read first? — owner: capstone owner, due: Collection feature brief
- [ ] From what team size is a team value effectively personal? — owner: capstone owner, due: Evidence Guard feature PRD
- [ ] Who reviews and publishes the monthly page (role, and whether it is the Lead)? — owner: capstone owner, due: Reporting feature brief

## Related
- [SPEC.md](../SPEC.md) — v1 goals, non-goals, acceptance criteria
- [docs/bc-map.md](bc-map.md) — contexts, events, glossary
- [F1 brief](features/metric-computation/idea-brief.md) and [F1 CONTEXT](features/metric-computation/CONTEXT.md)

## DoD self-check
- [x] 15 sections present
- [x] No anti-pattern terms (datastore, broker, library names)
- [x] Length ≤ 5 pages
- [x] Frontmatter status: Confirmed
- [x] RICE confirmed (state: confirmed)
- [x] Feasibility confirmed (state: confirmed; Time open)
- [x] Recommendation present with rationale citing §6, §8, §11, §12
