---
status: Draft | Confirmed | Frozen
owner: "<role, not a person's name>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: <XS|S|M|L|XL>     # set by sdlc:classify-size, not here
stage: "01"
depth: easy | medium | hard   # interview depth used
ticket: "<ticket-id>"
value_score:
  rice: <number>                 # computed by Claude
  state: proposed | confirmed
  confirmed_at: "<YYYY-MM-DD>"
feasibility_state: proposed | confirmed
---

<!-- Stage 01 → produced by brief-builder (docs/skills-draft/brief-builder/SKILL.md) -->
<!-- Why: capture the idea before it's forgotten or retold incorrectly -->

<!-- Self-check (not user-visible): no datastore, broker, framework or library names, no
     table schemas, endpoints, latency targets; no organisation, client or person names.
     This is a PRODUCT brief; tech lives in the PRD NFRs, the SAD and ADRs. -->

# Idea Brief — <feature name>

## 1. Raw idea
<1 paragraph verbatim from user, phase 1>

## 2. Problem
<1-3 sentences, facts/numbers>

## 3. Users
<who suffers, frequency, segments>

## 4. Why now
<trigger: incident/contract/deadline>

## 5. Out of scope
- bullet

## 6. Competitive analysis
| # | Product · URL | Features | Value per feature (1-5) | Gap |
|---|---|---|---|---|
| 1 | <name> · <url> | <features> | <ratings> | <gap> |
| 0 | Status quo: <manual process / nothing> | <what people do today> | <ratings> | <why it fails> |

Footnotes per row: date, search query, and **fetched** or **snippet only**.

## 7. Strategic approaches

### Approach A — <3-5 word name>
- **Thesis** (1 sentence, product language)
- **For whom** (which segment from §3 benefits most)
- **Outcome metric** (1 KPI: baseline → target)
- **Key trade-off** (1 line)
- **Effort signal**: S / M / L
- **Recommended?** ◯ / ●  (filled in §13)

### Approach B — ...
[same structure]

### Approach C — ...
[same structure]

## 8. Multi-perspective feedback

### Engineer
- 3-5 bullets (concerns / value / risks — abstract, NO library or DB names)

### Executive
- 3-5 bullets

### UX-researcher
- 3-5 bullets

### Synthesis matrix
|         | Engineer | Executive | UX |
|---------|:--------:|:---------:|:--:|
| App. A  | +        | +         | 0  |
| App. B  | -        | +         | -  |
| App. C  | 0        | 0         | +  |

6-word justifications in each cell.

## 9. Trade-offs and edge cases

### Trade-offs per approach
| Approach | Pros | Cons |
|---|---|---|
| A | ... | ... |
| B | ... | ... |
| C | ... | ... |

### Edge cases
- 5-8 items

## 10. Risks
- Top devil's advocate attack vector (from phase 8)
- Other identified risks

## 11. RICE — Claude proposed
- **Reach (R)**: <units of work per quarter, e.g. team-months> — rationale cites §3 Users
- **Impact (I)**: <0.25 | 0.5 | 1 | 2 | 3> — rationale cites Executive perspective + Problem severity (§2, §8)
- **Confidence (C)**: <0.5 | 0.7 | 0.8 | 1.0> — rationale cites count of TBDs / Open questions (§15)
- **Effort (E)**: <person-weeks> — rationale cites Effort signal from §7
- **RICE = R × I × C / E = <number>**
- **State**: proposed | confirmed

## 12. Feasibility — Claude proposed

- [☑/☐] **Tech**: <rationale — cite adjacent feature from repo scan>
- [☑/☐] **Skills**: <rationale>
- [☑/☐] **Time**: <rationale — cite similar past feature shipping time>
- **State**: proposed | confirmed

## 13. Recommendation
**Selected: Approach <X>** — <3-5 sentence rationale>

Rationale MUST cite:
- RICE score from §11
- Feasibility state from §12
- ≥1 multi-perspective cell from §8
- ≥1 competitive gap from §6

**Locked-in pointer**: <what this commits us to for write-spec phase>

## 14. Parked & rejected approaches
| # | Approach | Status | Reason | Revisit trigger |
|---|---|:---:|---|---|
| B | <name> | parked | <reason> | <trigger> |
| C | <name> | parked | <reason> | <trigger> |
| - | <name> | rejected | <reason> | - |

## 15. Open questions
- [ ] <question> — owner: <name>, due: <date>
- [ ] ...

## 16. Data and people
- **Data read**: <which sources, at what level (team, service, month)>
- **Could the output identify or rank a person?** <no, because … / yes → stop: redesign or drop>
- **Public-safety**: <what stays outside the repository (private definitions, identifiers)>

## 17. Evidence of the pain
- **Baseline**: <measured value + how and when / estimated by whom>
- **First measurement**: <who measures the baseline, by when> (copied to §15 if not measured)

## Related
- Links to CONTEXT.md, ticket, related features

## DoD self-check
- [ ] 17 sections present (incl. §16 Data and people, §17 Evidence of the pain)
- [ ] No stack or library names; no organisation or person names
- [ ] §6 has a status-quo row and fetched/snippet marks
- [ ] Length ≤ 5 pages (~2400 words)
- [ ] Frontmatter status: Confirmed
- [ ] RICE confirmed (state: confirmed)
- [ ] Feasibility confirmed (state: confirmed)
- [ ] Recommendation present with rationale citing 4 upstream sections (§6, §8, §11, §12)
