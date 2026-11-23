---
status: Confirmed
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-23"
feature_size: TBD     # set by sdlc:classify-size, not here
stage: "01"
depth: easy
ticket: "none (comparison run of brief-builder; the canonical brief is idea-brief.md)"
value_score:
  rice: 7.5
  state: confirmed
  confirmed_at: "2026-11-23"
feasibility_state: confirmed
---

<!-- Stage 01 → produced by brief-builder (docs/skills-draft/brief-builder/SKILL.md), easy depth, 2026-11-23.
     Comparison run for homework m06-l02; idea-brief.md (plugin interview, hard) stays canonical. -->

# Idea Brief — metric-computation (brief-builder run)

## 1. Raw idea
Give a lead the first metric for one team and one closed month in under five minutes, with the definition
version and inputs attached.

## 2. Problem
Leads count metrics by hand from the written guide; the work takes hours per team-month, so it is late or
skipped, and nothing systematic exists. The size is an owner estimate (§17).

## 3. Users
Leads run it monthly for the teams they own (pilot: about 5 teams); engineering managers read the values on
the reviewed monthly page.

## 4. Why now
The guide is new and the first months set the baseline; the capstone gives a fixed window this month.

## 5. Out of scope
- A second metric; a run over all teams; drill-down to records; reading the live tracker; per-person values.

## 6. Competitive analysis
| # | Product · URL | Features | Value per feature (1-5) | Gap |
|---|---|---|---|---|
| 1 | Apache DevLake · https://devlake.apache.org/docs/Metrics | Delivery metrics from tracker + Git | 4 | Own fixed metric variants; no definition version shown per value |
| 2 | Four Keys · https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance | Delivery metrics pipeline from repository events | 3 | Fixed definitions; a cloud pipeline to run, not a monthly closed-snapshot run |
| 3 | Middleware · https://github.com/drupalio/middleware | Team-level delivery metrics from repository data | 3 | Simplified fixed rules (e.g. reverts as incidents); no versioned definitions |
| 0 | Status quo: nothing systematic | Values counted by hand when asked | 1 | Late, skipped, and depends on who counts |

Footnotes: all rows 2026-11-23, query "open source engineering metrics tool versioned metric definitions
team-level DORA"; rows 1-3 **snippet only**. Vendors also differ in how they compute the same metric (mean vs
median), which is the case for versioned definitions.

## 7. Strategic approaches
- **A — One team, one number** (S): a lead names team and month and gets the value stamped with definition version and inputs. Outcome: estimated hours → under 5 minutes per team-month. Trade-off: one run per team. **Recommended.**
- **B — Every number explains itself** (L): drill-down from value to records and side-by-side recompute across versions. Outcome: TBD. Trade-off: misses the week; person-leak risk.
- **C — Whole portfolio** (M): one run for all teams of a month, reproducible. Outcome: under 5 minutes per month for all teams. Trade-off: over the week; partial-failure handling.

## 8. Multi-perspective feedback
|         | Engineer | Executive | UX |
|---------|:--------:|:---------:|:--:|
| App. A  | + one pure formula, golden-testable | + fits week, proves traceability | 0 simple, repeated per team |
| App. B  | − lineage plus person-leak risk | − misses window, no outcome | + most trust for readers |
| App. C  | 0 partial failures, re-run testable | 0 right unit, over budget | + one action a month |

## 9. Trade-offs and edge cases
- A is the smallest and fits the time box; C fits how leads work; B builds trust but is too big.
- Edge cases: teams use tracker states differently; a definition edited without a new version; missing data shown as zero; a version change between two teams' runs.

## 10. Risks
- **Top: a believable wrong number** — the stamp makes a value look verified when per-team tracker use differs (standard risk 1 of the skill).
- Per-person leak through a tiny team (§16); a version label that lies; zero for missing data.

## 11. RICE — Claude proposed, owner confirmed
- Reach 15 team-months per quarter (§3, pilot 5 teams × 3 months); Impact 1 (§2, one metric of several);
  Confidence 0.5 (§17 estimated pain, first metric not chosen); Effort 1 person-week (§7, signal S).
- **RICE = 15 × 1 × 0.5 / 1 = 7.5** (C 1.9, B 0.9). State: confirmed.

## 12. Feasibility — Claude proposed, owner confirmed
- [TBD] Tech: `src/evidence_meter/computation/` is an empty skeleton; no snapshot source before Collection.
- [☑] Skills: S5 built `platform/migrate.py` and `tests/test_architecture.py` with the same toolchain.
- [☑] Time: S5 shipped in one day (2026-11-22).
- State: confirmed (Tech TBD).

## 13. Recommendation
**Selected: Approach A.** RICE 7.5 against 1.9 and 0.9 (§11); Skills and Time confirmed, Tech open until
the snapshot source is decided (§12); the engineer view rates it "+ one pure formula, golden-testable" (§8);
none of the tools found shows a definition version on each value, and the status quo computes nothing
until asked (§6). **Locked-in pointer**: one metric, one team, one closed month, stamped with version and inputs.

## 14. Parked & rejected approaches
| # | Approach | Status | Reason | Revisit trigger |
|---|---|:---:|---|---|
| B | Every number explains itself | parked | Size L, person-leak risk | Managers question values at review |
| C | Whole portfolio | parked | Over the one-week time box | A in use for 5+ teams a month |

## 15. Open questions
- [ ] Which metric is first? — owner: capstone owner, due: 2026-11-24
- [ ] Measure one team-month by hand (§17) — owner: capstone owner, due: 2026-11-30
- [ ] Snapshot source before Collection exists — owner: capstone owner, due: S7 (SAD)
- [ ] Minimum team size for a team value (§16) — owner: capstone owner, due: Evidence Guard feature

## 16. Data and people
- **Data read**: one stored snapshot of tracker and Git data, per team and month.
- **Could the output identify or rank a person?** No: values are per team and month. A one- or two-person team is an open risk (§15) handled by Evidence Guard.
- **Public-safety**: metric codes, thresholds and identifiers stay in the private definitions file outside git.

## 17. Evidence of the pain
- **Baseline**: "hours per team-month by hand" is estimated by the owner, not measured.
- **First measurement**: the owner times one team-month by hand by 2026-11-30 (§15).

## Related
- [idea-brief.md](idea-brief.md) — canonical brief from the plugin interview (hard depth)
- [CONTEXT.md](CONTEXT.md) — glossary

## DoD self-check
- [x] 17 sections present (incl. §16 Data and people, §17 Evidence of the pain)
- [x] No stack or library names; no organisation or person names
- [x] §6 has a status-quo row and fetched/snippet marks
- [x] Length ≤ 5 pages (~2400 words)
- [x] Frontmatter status: Confirmed
- [x] RICE confirmed (state: confirmed)
- [x] Feasibility confirmed (state: confirmed)
- [x] Recommendation present with rationale citing 4 upstream sections (§6, §8, §11, §12)
