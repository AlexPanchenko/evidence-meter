---
status: Approved
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: "M"
stage: "03"
ticket: "none (capstone F1)"
---

# PRD — metric-computation

> **Inputs (required):** [idea-brief](./idea-brief.md) · [CONTEXT](./CONTEXT.md)
> **Reference module:** `src/evidence_meter/platform/migrate.py` — patterns used: applying again is a no-op that reports "nothing pending"; each change is all-or-nothing; a refusal lists the offending items (bad migration names).
> **External context channels used:** Project docs: `SPEC.md` (v1 acceptance criteria 2, 5, 7, 8), `docs/bc-map.md` (events, contexts), `docs/adr/0004-auth-oidc-deferred.md`, `src/evidence_meter/computation/README.md`; architecture-map: `docs/architecture-map.md`.

## 1. Context

A lead counts engineering metrics by hand from the written guide; it takes hours per team per month, so the
work is done late or skipped, and nothing systematic exists (idea-brief §2). Leads run the count for the
teams they own, roughly 5-15 teams; engineering managers read the values on the reviewed monthly page
(idea-brief §3).

The guide has just been written and the first months set the baseline everyone compares against; the
capstone gives a fixed delivery window this month (idea-brief §4).

Committed approach — **One team, one number** (idea-brief §13): a lead names one team and one closed period
and gets the first metric, cycle time, stamped with the definition version, the state map and the inputs it
used. The core is built so that running it over all teams later is cheap.

Traceability:
- Reference patterns from `platform/migrate.py` shaped AC-03 (a repeat is a no-op that says so), AC-04 (a
  refusal lists the offending items) and NFR-5 (all-or-nothing).
- The interview ran at depth hard, but the ideation suite (research, approaches, review, devil's advocate) was
  not rerun: its results in idea-brief §6-§10, from the same day, were reused.
- Owner decisions in the deep-dive: per-team state maps (idea-brief §10 top risk); reopened work counts per
  pass, the later pass starting at the reopen; a re-run returns the same measurement; the lead sees an
  unchecked measurement before Evidence Guard exists; a missing snapshot is refused, never shown as zero.
- Critic pass: AC-01b moved to US-01 (a formula result with no defined median, not a refusal, so the
  all-or-nothing NFR holds) and names the definition id; CONTEXT.md Measurement covers the no-value case.

## 2. Goals

- A lead gets a team's cycle time for a closed month without counting by hand.
- Every value can be traced to its definition version, state map and inputs, and recomputing it gives the
  same result.
- When the data cannot support a value, the lead gets a plain reason, never a misleading number or a zero.

## 3. Non-goals

- A second metric — it is F2, built later through the plugin, so F1 stays one thin slice.
- Computing all teams in one run — approach C is parked until approach A is in use for 5+ teams a month.
- Drill-down from a value to individual issues — approach B is parked: it is size L and risks exposing a person.
- Refusing values on thin data or low coverage — that decision belongs to Evidence Guard, a later feature.
- Putting a value on the monthly page — Reporting accepts only values with a Verdict.
- Any value, column or log line per person — the tool must not become a ranking of people (SPEC non-goals).

## 4. User stories

### US-01: Compute a team's cycle time
**As a** Lead
**I want** to compute cycle time for one team and one closed period
**So that** the value no longer takes hours of counting by hand

### US-02: See what made the value
**As a** Lead
**I want** to see the definition version, state map and inputs behind a value
**So that** nobody argues about how it was counted

### US-03: Re-run and get the same
**As a** Lead
**I want** a re-run of a computed team and period to give the identical value
**So that** anyone can confirm a value by computing it again

### US-04: Learn why nothing was computed
**As a** Lead
**I want** a plain reason when a value cannot be computed
**So that** I fix the gap instead of reading it as zero

### US-05: Count reopened work per pass
**As a** Lead
**I want** each finished pass counted in the period of its own done
**So that** reopened work is neither lost nor counted twice

### US-06: Keep results team-level
**As a** Lead
**I want** any breakdown by person to be refused
**So that** the tool cannot become a ranking of people

### US-07: Respect retired definitions
**As a** Lead
**I want** a retired definition version to be refused for new computations while old values keep naming it
**So that** a retired definition never produces new numbers and history is not rewritten

## 5. Acceptance criteria

### AC-01 (US-01) — happy path
**Given** a closed snapshot for team-alpha and period 2026-10, a published cycle-time definition version, and a state map that covers every state team-alpha uses
**When** the Lead computes cycle time for team-alpha and 2026-10
**Then** the system records the measurement — the median duration of the passes finished in 2026-10 — and shows it to the Lead marked as not yet checked by Evidence Guard

### AC-01b (US-01) — domain invariant (edge case: no finished passes)
**Given** team-alpha finished no passes in 2026-10, because every issue is still open or excluded
**When** the Lead computes cycle time for team-alpha and 2026-10
**Then** the system records a measurement stating that no passes were finished, so the median is not defined; it shows no number and no zero, and names the definition id, the definition version and the inputs. This is a formula result, not a refusal: judging thin data stays with Evidence Guard

### AC-02 (US-02) — happy path (traceability)
**Given** the measurement from AC-01
**When** the Lead looks at it
**Then** it names the definition id, the definition version, the state map, the number of passes counted and the number of issues excluded as won't-do or duplicate, and nothing that identifies a person

### AC-03 (US-03) — domain invariant
**Given** a recorded measurement for team-alpha, 2026-10 and definition version 1
**When** the Lead computes again with the same snapshot and the same definition version
**Then** the system shows the identical value and inputs, says it matches the earlier measurement and records no second one; if the new result differed, it would report a defect instead of showing either value

### AC-04 (US-04) — error
**Given** team-alpha has issues in a tracker state its state map does not cover
**When** the Lead computes cycle time for team-alpha and 2026-10
**Then** the system computes and records nothing and lists the unmapped states so the Lead can extend the state map

### AC-05 (US-04) — error
**Given** no private definitions file is present
**When** the Lead computes cycle time for any team and period
**Then** the system stops with a message that the definitions file is missing and records nothing

### AC-06 (US-01) — error
**Given** the period is not closed yet, for example the current month
**When** the Lead computes cycle time for it
**Then** the system refuses and tells the Lead that the period must be closed first

### AC-07 (US-04) — cross-context
**Given** no closed snapshot exists for team-beta and 2026-10
**When** the Lead computes cycle time for team-beta and 2026-10
**Then** the system computes nothing, tells the Lead that collection must run for that team and period first, and never shows zero

### AC-08 (US-05) — domain invariant
**Given** an issue of team-alpha was finished in 2026-09, reopened in 2026-10 and finished again in 2026-10
**When** the Lead computes cycle time for team-alpha and 2026-10
**Then** 2026-10 counts one pass for that issue, from the reopen to the second done, and the recorded measurement for 2026-09 is unchanged

### AC-09 (US-06) — authorization
**Given** any team and any period
**When** the Lead asks for cycle time broken down by person
**Then** the system refuses with the reason that results are team-level only, and nothing per person is recorded, shown or logged

### AC-10 (US-07) — cross-context
**Given** cycle-time definition version 1 was retired in Definitions and version 2 is published
**When** the Lead computes cycle time with version 1
**Then** the system refuses, names version 2 as the current version, and the existing version 1 measurements stay unchanged and still name version 1

## 6. Non-functional requirements

| Aspect | Target | Measurement |
|---|---|---|
| Run time for one team and period, snapshot up to 5,000 issues | ≤ 10 s on a developer laptop | timed test in CI on a synthetic 5,000-issue snapshot |
| Reproducibility | 100% identical value and inputs on re-run | re-run test over the golden data in `make check` |
| Offline | 0 network calls during computation | test with network access blocked (SPEC acceptance criterion 8) |
| Per-person data in outputs | 0 per-person fields in command output, records or logs | a test scans every output (SPEC acceptance criterion 5) |
| All-or-nothing | 0 partial records after a refused or failed run | test that every refusal AC leaves the store unchanged |

## 6.1 Security / privacy

- **Data classification:** internal — the snapshot holds a team's tracker history.
- **Personal data touched:** the snapshot may carry assignees and authors; F1 reads states and timestamps only and outputs no field per person.
- **AuthZ/AuthN impact:** no sign-in; F1 runs locally (ADR 0004). The one capability rule is "results are team-level only" (AC-09).
- **Abuse cases:**
  - Breakdown by person requested: refused, nothing recorded (AC-09).
  - A team of one or two people: its team value is effectively one person's value; handled by Evidence Guard (§8).
  - Private state names or definition codes leaking into committed files: they are shown only to the local lead, never written to the repository.
  - Serving the value to other machines: F1 stays local; serving data makes F1 the first data-serving feature, which brings sign-in (§8).
- **Security review:** Required — size M and a new boundary around person data in the snapshot.

## 7. Metrics / KPIs

- **Lead's time per team and period to the first metric** — baseline: hours, estimated, not measured (the owner times one team-month by hand by 2026-11-30); target: ≤ 5 minutes within the first closed month after release.
- **Pilot teams with a computed value each month** — baseline: 0; target: 5 within two closed months after release.
- **Share of runs refused for unmapped states** — baseline: TBD, measured over the first closed month after release; target: ≤ 10% of runs from the second month.

## 8. Open questions

- [ ] How does F1 get a closed snapshot before Collection exists? Default now: a synthetic stored snapshot. — owner: capstone owner, due: S7 (`/sdlc:architecture-design`)
- [ ] Does F1 offer the value through the local API, which would make it the first data-serving feature and bring sign-in (ADR 0004)? Default now: command line only. — owner: capstone owner, due: S7 (`/sdlc:architecture-design`)
- [ ] From what team size is a team value effectively personal? Default now: no limit in F1. — owner: capstone owner, due: Evidence Guard feature PRD
- [ ] What is the by-hand baseline for one team and period? Default now: "hours", estimated. — owner: capstone owner, due: 2026-11-30
