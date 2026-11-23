---
status: Approved
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: "M"
contexts: ["computation", "definitions", "collection"]
skill: prd-builder
ticket: "none (capstone F1)"
---

# PRD — metric-computation

> **Inputs (required):** [idea-brief](./idea-brief.md) · [CONTEXT](./CONTEXT.md)
> **Reference module:** `src/evidence_meter/platform/migrate.py` — patterns used: idempotent repeat («nothing pending»), all-or-nothing per change, a refusal that lists the offending items.
> **Other channels used:** [SPEC.md](../../../SPEC.md) goals 2-3 and acceptance criteria 2, 3, 5, 7, 8; [docs/bc-map.md](../../bc-map.md); [ADR 0001](../../adr/0001-stack.md), [0002](../../adr/0002-modular-monolith.md), [0003](../../adr/0003-persistence-sqlite.md), [0004](../../adr/0004-auth-oidc-deferred.md).

**Feature in one sentence (owner's wording):** A lead names one team and one closed month and gets its cycle time, stamped with the definition version and the inputs it used.

## 1. Context

Collecting and computing engineering metrics by hand from the written guide takes a lead several hours per
team per month (owner's estimate, not measured), so it is done late or skipped, and values are computed ad
hoc when someone asks. The lead runs the monthly numbers for the 5-15 teams they own; engineering managers
read the team values on the reviewed monthly page. The subject of every value is a team, never a person.

The metrics guide has just been written. Without a tool it will be applied inconsistently from the first
month, and the first months set the baseline everyone compares against. The capstone gives a fixed window:
one person, part-time, about one week from spec to working code.

The committed approach is **Approach A — One Team, One Number** (idea-brief §13): for one team and one
closed period, compute the first metric, cycle time, from a versioned definition and record it as a
Measurement that names its definition id, definition version and inputs. Looping over all teams (approach C)
and drill-down to records (approach B) are parked; the core is built so that C is cheap next.

Traceability:
- Reference `platform/migrate.py`: «applying again says nothing pending» → AC-10; «each change all-or-nothing» → §6 All-or-nothing and every error AC; «a refusal lists the offending items» → AC-05.
- Owner decision (deep-dive): a repeat with the same inputs returns the stored Measurement; a repeat with different inputs stops and records nothing (AC-10, AC-11). Correcting a value needs a new definition version.
- Owner decision (deep-dive): a tracker state the team's state map does not cover stops the run and lists every such state (AC-05). This answers the state-mapping part of idea-brief §15 «per-team tracker differences» and the top risk «a believable wrong number»; sub-tasks and duplicates stay open in §8 with a default.
- Owner decision (deep-dive): inputs recorded next to the value are team aggregates only, no issue keys, no people (AC-03, AC-13, §9).
- Owner decision: depth easy; channels `platform/migrate.py` and ADRs 0001-0004.
- Assumption (easy depth): F1 has no API or web surface; the lead runs it from the command line. Serving data waits for sign-in (ADR 0004).
- Assumption (easy depth): which teams may be computed is set by the private definitions file (a team without a state map there is not computable, AC-09); there is no other access control on a local single-user tool.
- Assumption (easy depth): durations are calendar time and the month boundary is in UTC; both are open questions in §8.
- Assumption (easy depth): the small-team rule belongs to Evidence Guard; F1 computes for any team size (§9).
- Assumption (easy depth): the Lead names only a team and a period; the system uses the latest published cycle time version (AC-01, AC-08).
- Critic pass: 4 findings, all accepted. Sub-tasks and duplicates moved to a §8 question with a default (F3); AC-11 now names a newer snapshot instead of a changed one, since snapshots are immutable (F5); AC-08 dropped the Lead's version choice and its message no longer advises an impossible step (F5); AC-12 now passes definition id and snapshot to Evidence Guard (F5).

## 2. Goals

- A lead gets the cycle time for one team and one closed month without counting by hand.
- Every value can be traced to the definition version and the inputs it came from, and a repeat run on the same snapshot gives the same value.
- A run that cannot produce a trustworthy value stops and says what to fix, instead of producing a believable wrong number.

## 3. Non-goals

- A second metric — F1 is exactly one metric end to end; the next one is F2.
- Running all teams in one go — approach C, parked until leads run it for 5+ teams a month (idea-brief §14).
- Drill-down from a value to the issues or passes behind it — approach B, parked; it opens a person-identification path.
- Reading the live tracker or Git — the Collection context does that; F1 reads a stored snapshot.
- Deciding whether a value may be shown — the Evidence Guard context decides, after F1.
- Showing the value on a page, over the API or in the web app — the Reporting context and the sign-in feature (ADR 0004).
- Any value, column or log line per person — the tool must not become a ranking of people.

## 4. User stories

### US-01: Compute cycle time for a team-month
**As a** Lead
**I want** to name one team and one closed period and get its cycle time
**So that** I stop counting it by hand from the guide

### US-02: See what a value came from
**As a** Lead
**I want** each Measurement to name its definition id, definition version and inputs
**So that** nobody argues about how the number was counted

### US-03: Learn why no value was produced
**As a** Lead
**I want** a run that cannot compute to stop and tell me what to fix
**So that** I never see a believable wrong number

### US-04: Repeat a run safely
**As a** Lead
**I want** running the same team and period again to give the same Measurement
**So that** a second run neither changes nor duplicates a value

### US-05: Hand the value to Evidence Guard
**As a** Lead
**I want** a new Measurement to go to Evidence Guard and stay marked not yet checked until it rules
**So that** no unchecked value reaches a page

### US-06: Keep the team as the subject
**As a** Lead
**I want** the Measurement to carry no person's data
**So that** the tool cannot be used to rank people

## 5. Acceptance criteria

### AC-01 (US-01) — happy path · result
**Given** the private definitions publish cycle time version 1 with a state map for team-alpha, and a stored snapshot for team-alpha and period 2026-10 in which four passes finished in October with durations of 2, 3, 5 and 10 days
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** the system records one Measurement of 4.0 days (the median of the four passes), shows it with definition id, definition version 1 and its inputs, and marks it not yet checked

### AC-01b (US-01) — domain invariant · result
**Given** an issue in the team-alpha snapshot whose first pass finished in September 2026 and which was reopened and finished again in October 2026
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** only the October pass counts towards the median, measured from the reopen to the second done

### AC-01c (US-01) — domain invariant · result
**Given** in the team-alpha snapshot one pass ended in a state the state map calls excluded and one pass was started in October but not done by the end of the month
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** neither pass counts towards the median, and the excluded one is counted in the issues-excluded input

### AC-02 (US-01) — happy path · result
**Given** a stored snapshot for team-beta and period 2026-10 in which no pass finished in October
**When** the Lead runs the computation for team-beta and 2026-10
**Then** the system records a Measurement with no value, says «no passes finished in 2026-10», and shows no number and no zero

### AC-03 (US-02) — domain invariant · result
**Given** any Measurement recorded by this feature
**When** the Lead looks at it
**Then** it names the definition id, the definition version, the snapshot it was read from and the inputs: issues considered, passes finished and issues excluded

### AC-04 (US-03) — error · error
**Given** no stored snapshot exists for team-alpha and period 2026-10
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** the system stops, records nothing, and says that there is no snapshot for team-alpha in 2026-10 and that one must be collected first

### AC-05 (US-03) — error · error
**Given** the team-alpha snapshot has issues in the tracker states «Blocked» and «In QA», which the team-alpha state map does not cover
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** the system stops, records nothing, and lists both unmapped states so the Lead can add them to the state map

### AC-06 (US-03) — error · error
**Given** today is 2026-11-23, so period 2026-11 is not closed
**When** the Lead runs the computation for team-alpha and 2026-11
**Then** the system stops, records nothing, and says that 2026-11 is not a closed period yet

### AC-07 (US-03) — error · error
**Given** there is no private definitions file on the Lead's machine
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** the system stops, records nothing, and says where it expected the definitions file

### AC-08 (US-03) — cross-context · error
**Given** the Definitions context has retired cycle time version 1 and published no newer version
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** the system stops, records nothing, says cycle time version 1 is retired and no published version exists, and leaves every Measurement already recorded with version 1 as it was

### AC-09 (US-03) — authorization · error
**Given** the private definitions hold state maps for team-alpha and team-beta only
**When** the Lead runs the computation for team-gamma and 2026-10
**Then** the system stops, records nothing, and says that team-gamma has no state map in the definitions, so it cannot be computed

### AC-10 (US-04) — happy path · result
**Given** a Measurement for team-alpha, 2026-10 and cycle time version 1 is already recorded from the same snapshot
**When** the Lead runs the computation for team-alpha and 2026-10 again
**Then** the system says it is already computed, shows the stored Measurement unchanged, and records nothing new

### AC-11 (US-04) — error · error
**Given** a Measurement for team-alpha, 2026-10 and cycle time version 1 is already recorded, and a newer snapshot for team-alpha and 2026-10 gives different inputs
**When** the Lead runs the computation for team-alpha and 2026-10 again
**Then** the system stops, records nothing, keeps the stored Measurement, and shows both input sets side by side

### AC-12 (US-05) — cross-context · result
**Given** the system has just recorded the Measurement for team-alpha and 2026-10
**When** the computation finishes
**Then** Evidence Guard is told that a value was computed, with its team, period, definition id, definition version, snapshot and inputs, and until Evidence Guard returns a Verdict the Lead sees the value marked not yet checked and no monthly page shows it

### AC-13 (US-06) — domain invariant · result
**Given** a snapshot for team-alpha whose issues carry assignees and authors
**When** the Lead runs the computation for team-alpha and 2026-10
**Then** the recorded Measurement, what the Lead sees and every log line contain team-level values only: no person's name, identifier or per-person count

## 6. Non-functional requirements

| Aspect | Target | Measurement |
|---|---|---|
| Command run time, one team and period | ≤ 10 s for a 5,000-issue snapshot on a developer laptop | timed test on a synthetic snapshot |
| API read latency p95 | N/A — F1 has no API surface; serving data waits for sign-in (ADR 0004) | — |
| Reproducibility | 100% identical value and inputs on re-run over the same snapshot | re-run test over golden data |
| Golden data | cycle time has hand-computed expected values covering odd and even pass counts, reopen, excluded, no passes | golden-data tests in `make check` (SPEC 3) |
| Offline | 0 network calls in computation and in `make check` | network-blocked test (SPEC 8) |
| Per-person data | 0 per-person fields in command output, stored Measurement, logs | output scan test (SPEC 5) |
| All-or-nothing | 0 partial records after each of AC-04, 05, 06, 07, 08, 09, 11 | store-unchanged test per error AC |
| Migration | the Measurement table's forward migration has a rollback that restores the schema | up/down test |
| Availability / throughput | N/A — local single-user tool until sign-in (ADR 0004) | — |

## 6.1 Security / privacy

- **Classification:** Internal — team-level delivery data; no person is a subject of the output.
- **Personal data in inputs:** the snapshot may carry assignees, authors and reviewers. F1 reads only issue identity within the snapshot, state changes and their timestamps; it reads no person field and stores none (AC-13).
- **AuthZ impact:** none new. The tool runs locally and binds to 127.0.0.1 (ADR 0004); which teams can be computed is set by the private definitions file (AC-09).
- **Abuse cases:**
  - A lead computes for a team of one or two to read one person's speed → F1 records the team value; Evidence Guard owns the small-team refusal (§9, §8).
  - Someone asks for the inputs per issue to find the slow assignee → inputs are aggregates only; drill-down is a non-goal.
  - The private definition is edited in place without a new version → open question in §8; F1 records the version it was given and cannot tell.
  - A recorded Measurement is overwritten with a nicer value → a repeat with different inputs stops (AC-11).
- **Security review:** Required (size M, and the feature reads data that can identify a person).

## 7. Metrics / KPIs

| KPI | Baseline | Target | Timeframe |
|---|---|---|---|
| Lead's time to produce cycle time for one team-month | several hours by hand (estimated; §8 measures it) | under 5 minutes | first pilot month, 2026-12 |
| Share of runs that stop with an error, per month | none (new) | ≤ 1 in 5 after the state maps are settled in the first month | pilot, 2026-12 to 2027-02 |
| Measurements where a manager's own count disagrees with the value | unknown (new) | 0 across the pilot (about 5 teams × 3 months) | pilot, 2026-12 to 2027-02 |

## 8. Open questions

- [ ] What is the measured by-hand time for one team-month? Default now: «several hours» (estimate). — owner: capstone owner, due: 2026-11-30
- [ ] How does F1 get a snapshot before Collection exists: a synthetic fixture or a minimal collection? Default now: a synthetic fixture. — owner: capstone owner, due: S7 (SAD)
- [ ] Are pass durations calendar time or working days, and to what precision is the value shown? Default now: calendar time, shown in days to one decimal. — owner: capstone owner, due: before the golden data (S7)
- [ ] Which time zone sets the month boundary for a pass's done? Default now: UTC. — owner: capstone owner, due: S7 (SAD)
- [ ] How are sub-tasks and duplicates counted? Default now: duplicates and won't-do reach excluded through the state map (AC-01c); a sub-task counts as its own issue. — owner: capstone owner, due: before the golden data (S7)
- [ ] How is a definition edited in place without a new version number detected? Default now: not detected in F1. — owner: capstone owner, due: Definitions feature
- [ ] From what team size is a team value effectively one person's value? Default now: no limit in F1; Evidence Guard decides. — owner: capstone owner, due: Evidence Guard feature

## 9. Data and people

1. **Inputs that can identify a person:** the snapshot may hold assignees, authors and reviewers on issues. F1 does not read them; it reads issue identity within the snapshot, state changes and timestamps only.
2. **Outputs and their level:** one Measurement per team, period and definition version, with team aggregates as inputs (issues considered, passes finished, issues excluded) and the snapshot it came from. No value per person on any surface: command output — team only; stored record — team only; log lines — team, period and counts only; page — none in F1; API — none in F1.
3. **Small-team rule:** F1 sets no limit and computes for any team size. Whether a small team's value is effectively personal and must be refused is decided by Evidence Guard (§8).
4. **Synthetic data:** tests and examples use team-alpha, team-beta and team-gamma, period 2026-10 (and 2026-11 for the not-closed case), invented tracker states; never a real team, project key or person.
5. **Private definitions:** at run time F1 reads, through the Definitions context, the cycle time definition version and the team's state map from the private definitions file outside git. None of their contents is copied into the repository, a test, a log or a message; tests use a synthetic definitions file.

## 10. Errors and refusals

F1 has no refusal ACs: a refusal is a Verdict from Evidence Guard, which runs after F1 (AC-12).

| AC | Outcome class | Code or Verdict reason | Message the actor sees | Records anything? |
|---|---|---|---|---|
| AC-04 | error | `collection.snapshot_missing` | There is no snapshot for team-alpha in 2026-10; collect one first. | no |
| AC-05 | error | `computation.unmapped_states` | These tracker states are not in team-alpha's state map: Blocked, In QA. Add them and run again. | no |
| AC-06 | error | `computation.period_not_closed` | 2026-11 is not a closed period yet. | no |
| AC-07 | error | `definitions.file_missing` | No definitions file found at the expected location; create it and run again. | no |
| AC-08 | error | `definitions.version_retired` | Cycle time version 1 is retired and no published version exists. | no |
| AC-09 | error | `definitions.team_not_configured` | team-gamma has no state map in the definitions, so it cannot be computed. | no |
| AC-11 | error | `computation.measurement_conflict` | team-alpha, 2026-10, version 1 is already recorded with different inputs; both sets are shown. Nothing was changed. | no |

## 11. States and events

| Object (context) | Transition | Event | AC |
|---|---|---|---|
| Measurement (Computation) | none → recorded, not yet checked | `MetricComputed` | AC-01, AC-02, AC-12 |
| Measurement (Computation) | recorded → recorded with different inputs (forbidden) | — | AC-11 |
| Measurement (Computation) | recorded → recorded again with the same inputs (no change) | — | AC-10 |
| DefinitionVersion (Definitions) | retired → used for a new Measurement (forbidden); old Measurements keep naming it | `DefinitionVersionRetired` (listened to) | AC-08 |
| Snapshot (Collection) | read only; F1 never changes a snapshot | `TrackerSnapshotCollected` (listened to) | AC-04 |
| Verdict (Evidence Guard) | N/A — F1 only announces the value; the Verdict is Evidence Guard's feature | — | AC-12 |
