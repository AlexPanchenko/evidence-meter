---
status: Draft
owner: "capstone owner"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "2026-11-23"
feature_size: M
stage: "04-05"
ticket: "none (capstone F1)"
target_surfaces: [cli]  # filled in §4 — subset of: backend-service | web-frontend | mobile-app | desktop-app | cli | worker | library-sdk. Read (never re-derived) by api-forge/complete-sequence-diagrams/break-tasks/plan-tests/review-feature → _shared/surfaces.md
---

# Software Architecture Document — metric-computation (F1)

<!-- Stages 04-05 → see sdlc/plugin/skills/architecture-design/SKILL.md -->
<!-- 12 Arc42 sections. Empty sections — <!-- N/A: <one-line reason> -->. -->
<!-- C4 Context (L1) lives inline in §3. C4 Container (L2) lives inline in §5. -->
<!-- §6 Runtime view seeds the primary flow(s) here; complete-sequence-diagrams (stage 06) then -->
<!--    fills §6 with every critical flow / §5 AC — no cap. -->
<!-- Numbers in §10 come VERBATIM from PRD §6 NFR — no inventing, no rounding. -->

## 1. Introduction and goals

**Intent.** F1 lets a Lead compute one metric, cycle time (the median duration of the passes a team finished
in a period), for one team and one closed period, without counting by hand. Every value is recorded with
its definition id and version, the state map and the inputs it used, and computing it again gives the same
result. When the data cannot support a value, the Lead gets a plain reason, never a zero or a misleading
number. The core is built so that running it over all teams later is cheap (PRD §1, §2).

**Top-3 quality goals (1-liners; full scenarios in §10):**

1. **Reproducibility** — the same snapshot and definition version always give an identical value and inputs.
2. **Team-level only** — no value, field or log line per person, anywhere.
3. **Honest refusal, all-or-nothing** — a refused or failed run records nothing and gives a plain reason.

Run time (≤ 10 s for 5,000 issues) and offline computation (0 network calls) are quality requirements too;
they get §10 scenarios but do not override the three above.

**Stakeholders.**

| Role | Interest | Sign-off owner? |
|---|---|---|
| Lead | Runs the computation for their teams, reads the unchecked measurement | No |
| Engineering manager | Reads values later on the reviewed monthly page (Reporting); no F1 output | No |
| Tech Lead | Approves this SAD | Yes |
| Security Lead | Review required: size M, person data present in the snapshot (PRD §6.1) | Yes |

<!-- Decision overrides (¶4) — populated by the Step-7 critic resolution loop, empty otherwise. -->

## 2. Constraints

**Technical.**
- Python 3.12 with uv; standard library first. A new dependency needs the owner's OK and a licence and
  maintenance check (AGENTS.md).
- SQLite through the standard `sqlite3` module; plain SQL migrations `migrations/NNNN_<name>.up.sql` /
  `.down.sql` applied by `platform/migrate.py` ([repo ADR 0003](../../adr/0003-persistence-sqlite.md)).
- Modular monolith: five contexts, wired only in `entrypoints/`; the dependency rule is enforced by
  `tests/test_architecture.py` ([repo ADR 0002](../../adr/0002-modular-monolith.md)). Computation `domain`
  imports only the standard library and `shared`.
- CLI on argparse (`entrypoints/cli.py`); FastAPI exists with `/health` only and binds to 127.0.0.1 until
  OIDC sign-in ships ([repo ADR 0004](../../adr/0004-auth-oidc-deferred.md)).

**Organisational.**
- One developer (the capstone owner), AI-assisted.
- Design in week 1 (S7-S8, until 2026-11-26); implementation in week 2 (S9, 2026-11-27 to 2026-12-03).

**Conventions.**
- [AGENTS.md](../../../AGENTS.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md), [bc-map](../../bc-map.md)
  (contexts, events, glossary), [architecture-map](../../architecture-map.md) (current code).
- Failing test first; every metric gets golden data with expected values computed by hand.

**Regulatory / external.**
- The repository is public: synthetic data only in code, tests, fixtures and docs. An organisation's metric
  codes, thresholds and state names live in the private definitions file outside git
  (`~/.config/evidence-meter/`), read only by `definitions/`.
- Results are team-level only; nothing per person in outputs, records or logs (SPEC non-goals).
- The snapshot may carry assignees and authors, so a security review is required (PRD §6.1).

## 3. Context and scope

F1 runs on the Lead's machine as the `evidence-meter` CLI. It takes a team's snapshot from an imported
file and the definition version and state map from the private definitions file, and shows the Lead a
measurement in the terminal, marked as not yet checked. The issue tracker is not connected in F1
([ADR 0001](adr/0001-import-synthetic-snapshot-file-until-collection-adapter-exists.md)); Evidence Guard
and Reporting are internal contexts of later features and receive nothing from F1 beyond the published
`MetricComputed` event. Trust boundary: both files are outside the system and validated on read; nothing
leaves the machine.

**External systems (in / out):**

| Actor or system | Type | Interaction |
|---|---|---|
| Lead | Person | Imports a snapshot, computes cycle time, reads the unchecked measurement in the terminal |
| Snapshot file | External file (synthetic in the repo; a real export stays outside git) | Issues of one team with their state changes for one closed period; imported once, then immutable |
| Private definitions file | External file outside git (`~/.config/evidence-meter/`) | Definition versions, retirements and per-team state maps; read at run time |
| Issue tracker | External system, not connected in F1 | Source of real snapshots once Collection's adapter ships (a later feature) |

**C4 Context (L1):**

```mermaid
C4Context
    title Evidence Meter (F1 metric-computation) — System Context

    Person(lead, "Lead", "Runs the monthly computation for their teams")
    System(em, "Evidence Meter", "Computes team metrics from versioned definitions; local CLI in F1")
    System_Ext(snap, "Snapshot file", "One team's issue history for a closed period; synthetic in the repo")
    System_Ext(defs, "Private definitions file", "Definition versions, retirements, state maps; outside git")
    System_Ext(tracker, "Issue tracker", "Not connected in F1; read by Collection later")

    Rel(lead, em, "Imports snapshots, computes cycle time", "CLI")
    Rel(em, snap, "Imports once", "file read")
    Rel(em, defs, "Reads at run time", "file read")
    Rel(em, tracker, "Reads issues (later feature)", "HTTPS")
```

## 4. Solution strategy

**Target surface(s) (the first decision — what's being built):** `[cli]` — the `evidence-meter` command on
the Lead's machine. The API keeps `/health` only, so sign-in stays deferred
([ADR 0002](adr/0002-deliver-f1-as-cli-only-and-keep-api-health-only.md); closes PRD §8 open question 2).
No UI surface, so no UI-architecture decision.

**Top strategic choices (the seeds for ADRs):**

1. **Snapshot from an imported file, owned by Collection** — the tracker is not connected in F1; a snapshot
   file is imported once into Collection's store and is immutable from then on. Keeps F1 offline and
   credential-free, and tests use the same path as real runs (QG-1, offline NFR)
   ([ADR 0001](adr/0001-import-synthetic-snapshot-file-until-collection-adapter-exists.md)).
2. **Entrypoint orchestration with in-process events** — the compute command in `entrypoints/` asks
   Definitions for the version and state map, asks Collection for the snapshot, maps both into
   Computation's own input types and runs the use case; every refusal happens before anything is written
   (QG-3). `MetricComputed` goes to an in-process dispatcher with no listeners in F1
   ([ADR 0003](adr/0003-orchestrate-compute-in-entrypoints-with-in-process-events.md)).
3. **Reproducibility by identity** — a snapshot is identified by the sha256 of its canonical content; a
   measurement is unique on team, period, definition id, definition version and snapshot id. A re-run
   compares with the stored measurement: a match records nothing and says so, a difference is reported as a
   defect (QG-1, AC-03)
   ([ADR 0004](adr/0004-identify-snapshots-by-content-hash-and-measurements-by-natural-key.md)).
4. **Privacy by construction** — the import keeps issue keys, states and timestamps and drops assignee and
   author fields, so no person data is stored; a test scans every output, and a person breakdown is refused
   at the CLI (QG-2, AC-09) ([ADR 0005](adr/0005-drop-person-fields-at-snapshot-import.md)).
5. **Pure formula core** (repo convention, no ADR) — pass extraction, state-map application and the median
   are pure functions in `computation/domain/`, taking typed history and the state map as data; golden data
   with hand-computed values is the proof (bc-map, structure per context).

Each tactical decision in later sections should be traceable to one of these strategic seeds. Tactical
decisions that *contradict* a strategic choice are red flags — surface them in §11 Risks.

## 5. Building block view

Modular monolith in one Python process, following the repo: contexts are packages wired only in
`entrypoints/`; Computation is `domain/` → `app/` → `infra/`, the other contexts `handler/` → `service/`
→ `repo/` ([repo ADR 0002](../../adr/0002-modular-monolith.md)). F1 crosses three contexts (Collection,
Definitions, Computation) plus `shared`, `platform` and `entrypoints`; Evidence Guard and Reporting are not
touched. Each context owns its tables in the one SQLite file, prefixed by its name
([ADR 0006](adr/0006-prefix-tables-by-owning-context-in-one-sqlite-file.md)). The private definitions file
is TOML, read with the standard library's `tomllib` (no new dependency, comments allowed for a file the Lead
edits by hand).

**Internal decomposition:**

```
src/evidence_meter/
├── shared/          Team, Period, MetricComputed (event type)
├── platform/        config.py (env), db.py (one SQLite connection helper), migrate.py (exists)
├── collection/
│   ├── handler/     import a snapshot file; get a snapshot by team and period
│   ├── service/     parse and validate, drop person fields, canonicalise, sha256 id
│   └── repo/        collection_* tables
├── definitions/
│   ├── handler/     resolve a definition version and a team's state map
│   ├── service/     published vs retired, current version
│   └── repo/        private TOML file reader (tomllib)
├── computation/
│   ├── domain/      passes, state-map application, median, refusal reasons (pure, stdlib + shared)
│   ├── app/         compute use case; ports: MeasurementStore
│   └── infra/       computation_* tables
└── entrypoints/
    ├── cli.py       `snapshot import`, `compute cycle-time`; maps context results to Computation inputs
    └── dispatch.py  in-process event dispatcher (no listeners in F1)
```

**C4 Container (L2):**

```mermaid
C4Container
    title Evidence Meter (F1 metric-computation) — Containers

    Person(lead, "Lead", "Runs the monthly computation for their teams")

    Container_Boundary(em, "Evidence Meter") {
        Container(cli, "CLI (entrypoints)", "Python, argparse", "Commands; orchestrates a run; in-process events")
        Container(collection, "Collection", "Python package", "Imports, validates and stores immutable snapshots")
        Container(definitions, "Definitions", "Python package", "Resolves definition versions, retirements, state maps")
        Container(computation, "Computation", "Python package", "Pure cycle-time formula; records measurements")
        ContainerDb(db, "Local database", "SQLite", "collection_* and computation_* tables, schema_migrations")
    }

    System_Ext(snap, "Snapshot file", "Synthetic issue history for one team and period")
    System_Ext(defs, "Private definitions file", "TOML outside git")

    Rel(lead, cli, "Imports snapshots, computes cycle time", "terminal")
    Rel(cli, collection, "Import, get snapshot", "function call")
    Rel(cli, definitions, "Resolve version and state map", "function call")
    Rel(cli, computation, "Compute with mapped inputs", "function call")
    Rel(collection, snap, "Reads once", "file")
    Rel(definitions, defs, "Reads each run", "tomllib")
    Rel(collection, db, "Writes and reads collection_*", "sqlite3")
    Rel(computation, db, "Writes and reads computation_*", "sqlite3")
```

## 6. Runtime view

Seed flows from architecture-design; `complete-sequence-diagrams` adds the remaining flows (snapshot import,
person-breakdown refusal, reopened passes, period not closed) and the AC → flow coverage table. Participant
names are the §5 containers; messages are semantic, the command syntax comes with the CLI contract.

**Critical flow 1: compute cycle time and re-run (AC-01, AC-02, AC-03)**

```mermaid
sequenceDiagram
    actor Lead
    participant CLI
    participant Definitions
    participant Collection
    participant Computation
    participant DB as Local database
    Lead->>CLI: compute cycle time for team-alpha, 2026-10
    CLI->>Definitions: resolve current cycle-time version and team-alpha state map
    Definitions-->>CLI: definition id, version 1, state map
    CLI->>Collection: get the closed snapshot for team-alpha, 2026-10
    Collection->>DB: read collection_* rows
    Collection-->>CLI: snapshot id, issues with state changes
    CLI->>Computation: compute with mapped inputs
    Computation->>Computation: derive passes, apply state map, take the median (pure)
    Computation->>DB: look up measurement by team, period, definition, version, snapshot id
    alt no earlier measurement
        Computation->>DB: insert measurement (one transaction)
        Computation-->>CLI: recorded measurement
        CLI->>CLI: publish MetricComputed (in-process, no listeners in F1)
    else identical earlier measurement
        Computation-->>CLI: matches the earlier measurement, nothing recorded
    else different earlier measurement
        Computation-->>CLI: defect: re-run differs, neither value shown
    end
    CLI-->>Lead: value marked not yet checked, definition id and version, state map, passes counted, issues excluded
```

**Critical flow 2: refusal before any write (AC-04, AC-05, AC-07, AC-10)**

```mermaid
sequenceDiagram
    actor Lead
    participant CLI
    participant Definitions
    participant Collection
    participant Computation
    Lead->>CLI: compute cycle time for a team and period
    CLI->>Definitions: resolve version and state map
    alt definitions file missing
        Definitions-->>CLI: refused: definitions file missing (AC-05)
    else requested version retired
        Definitions-->>CLI: refused: version retired, current is version 2 (AC-10)
    else resolved
        Definitions-->>CLI: version and state map
        CLI->>Collection: get the closed snapshot
        alt no snapshot for team and period
            Collection-->>CLI: refused: import a snapshot for this team and period first (AC-07)
        else snapshot found
            Collection-->>CLI: snapshot
            CLI->>Computation: compute with mapped inputs
            Computation->>Computation: find tracker states the state map does not cover
            Computation-->>CLI: refused: unmapped states listed (AC-04)
        end
    end
    CLI-->>Lead: plain reason, non-zero exit; nothing recorded on any branch
```

## 7. Deployment view

<!-- N/A: F1 reuses the existing CLI deployment unit; no server, replicas or monitoring are added (target_surfaces: [cli], ADR 0002). -->

Deliberately not applicable for F1. The feature runs as the existing `evidence-meter` CLI on the Lead's
laptop, with the SQLite file at `$EVIDENCE_METER_DB` (default `var/evidence-meter.sqlite3`); the API is
unchanged and local-only. The only runtime target, ≤ 10 s for one team and period with up to 5,000 issues,
is verified in §10.

**Capacity note:** about 15 teams × 12 periods ≈ 180 snapshots a year of up to 5,000 issues each; one
SQLite file holds this comfortably, so no scaling threshold is set in F1. Revisit with the all-teams run
(PRD approach C).

## 8. Crosscutting concepts

| Concept | Convention | Where defined |
|---|---|---|
| Logging | Standard-library `logging` to stderr only, no log file; never a person field; private state names and definition codes appear only in the Lead's terminal output | here |
| Authentication | None: local CLI, the API stays `/health` only | [repo ADR 0004](../../adr/0004-auth-oidc-deferred.md), [ADR 0002](adr/0002-deliver-f1-as-cli-only-and-keep-api-health-only.md) |
| Capability rule | Team-level only; any breakdown other than team is refused with `person_breakdown` (AC-09) | AGENTS.md, here |
| Error and refusal model | A refusal is a `Refusal(code, message, details)` result from `shared/`, never an exception; closed code list: `definitions_missing`, `version_retired`, `snapshot_missing`, `unmapped_states`, `period_not_closed`, `person_breakdown`, `rerun_differs`; the CLI exits non-zero; unexpected failures stay exceptions | [ADR 0007](adr/0007-return-refusals-as-typed-results-with-stable-codes.md) |
| ID strategy | Snapshot id = sha256 of its canonical content; measurement unique on team, period, definition id, definition version, snapshot id | [ADR 0004](adr/0004-identify-snapshots-by-content-hash-and-measurements-by-natural-key.md) |
| Time and period | Timestamps normalised to UTC at import; a period is a UTC calendar month; a pass counts in the month of its done | [ADR 0008](adr/0008-use-utc-calendar-months-for-periods.md) |
| Transactions | One SQLite transaction per write command; every check runs before the first write (all-or-nothing) | here |
| Events | Event types in `shared/events.py`; in-process dispatcher in `entrypoints/dispatch.py`; `MetricComputed` has no listeners in F1 | [ADR 0003](adr/0003-orchestrate-compute-in-entrypoints-with-in-process-events.md) |
| Offline | No network import in Collection, Definitions or Computation; a test blocks sockets during compute | PRD §6, here |
| Privacy | Person fields dropped at snapshot import; a test scans command output, records and logs for person fields | [ADR 0005](adr/0005-drop-person-fields-at-snapshot-import.md) |
| Configuration | `platform/config.py`: `EVIDENCE_METER_DB` (exists) and `EVIDENCE_METER_DEFINITIONS` (path to the private TOML file, default under `~/.config/evidence-meter/`) | here |
| Internationalisation | English only | — |
| Observability | None beyond the run-time test in §10; local CLI | §7 |

## 9. Architecture decisions

| # | Title | Status | Section |
|---|---|---|---|
| [0001](adr/0001-import-synthetic-snapshot-file-until-collection-adapter-exists.md) | Import a synthetic snapshot file until Collection's tracker adapter exists | Accepted | §3 |
| [0002](adr/0002-deliver-f1-as-cli-only-and-keep-api-health-only.md) | Deliver F1 as a CLI only and keep the API health-only | Accepted | §4 |
| [0003](adr/0003-orchestrate-compute-in-entrypoints-with-in-process-events.md) | Orchestrate compute in entrypoints with in-process events | Accepted | §4 |
| [0004](adr/0004-identify-snapshots-by-content-hash-and-measurements-by-natural-key.md) | Identify snapshots by content hash and measurements by natural key | Accepted | §4 |
| [0005](adr/0005-drop-person-fields-at-snapshot-import.md) | Drop person fields at snapshot import | Accepted | §4 |
| [0006](adr/0006-prefix-tables-by-owning-context-in-one-sqlite-file.md) | Prefix tables by owning context in one SQLite file | Accepted | §5 |
| [0007](adr/0007-return-refusals-as-typed-results-with-stable-codes.md) | Return refusals as typed results with stable codes | Accepted | §8 |
| [0008](adr/0008-use-utc-calendar-months-for-periods.md) | Use UTC calendar months for periods | Accepted | §8 |

ADR files live under `docs/features/metric-computation/adr/NNNN-<title>.md`. Repository-wide decisions
(stack, modular monolith, SQLite, deferred sign-in) are in [docs/adr/](../../adr/).

## 10. Quality requirements

Each quality goal from §1, plus run time and offline, as a testable scenario. Numbers are verbatim from
PRD §6; test file names are proposals that `plan-tests` confirms.

**QG-1. Reproducibility**
- **When:** the Lead computes again a team and period already computed, with the same snapshot and the same definition version.
- **Then:** 100% identical value and inputs on re-run; the CLI says it matches the earlier measurement and records no second one; a difference is reported as `rerun_differs` and neither value is shown.
- **How verify:** re-run test over the golden data in `make check` (`tests/test_cycle_time_golden.py`).

**QG-2. Team-level only**
- **When:** any F1 command runs, including a request for a breakdown by person.
- **Then:** 0 per-person fields in command output, records or logs; the breakdown request is refused with `person_breakdown`.
- **How verify:** a test scans every output (SPEC acceptance criterion 5): command output, `collection_*` and `computation_*` rows and captured logs (`tests/test_privacy_outputs.py`).

**QG-3. Honest refusal, all-or-nothing**
- **When:** a run is refused (AC-04, AC-05, AC-06, AC-07, AC-09, AC-10) or fails.
- **Then:** 0 partial records after a refused or failed run; the Lead gets the plain reason for the refusal code.
- **How verify:** test that every refusal AC leaves the store unchanged, comparing the database contents before and after each case (`tests/test_refusals_leave_store_unchanged.py`).

**QG-4. Run time**
- **When:** the Lead computes one team and period from a snapshot of up to 5,000 issues.
- **Then:** ≤ 10 s on a developer laptop.
- **How verify:** timed test in CI on a synthetic 5,000-issue snapshot (`tests/test_compute_runtime.py`). CI stands in for the laptop, as the PRD states; a slower CI can only raise a false alarm, never hide a slowdown.

**QG-5. Offline**
- **When:** a compute run.
- **Then:** 0 network calls during computation.
- **How verify:** test with network access blocked (SPEC acceptance criterion 8): sockets patched to fail during compute (`tests/test_compute_offline.py`).

## 11. Risks and technical debt

<!-- 🎯 Навіщо: ⭐ збирає ВСЕ, що може зламатись — і не лише технічне. Без §11 ризики   -->
<!--           обговорюються на стендапах і губляться; борг лишається у голові того,    -->
<!--           хто його прийняв.                                                          -->
<!-- 📋 Що писати: таблиця ризик/борг — серйозність — мітигація — власник. Технічний    -->
<!--           борг окремою секцією.                                                      -->
<!-- 📌 Приклад: «EM не пушить — member не оновлює дані | High | …». Перший ризик —      -->
<!--           часто продуктовий, не технічний. Це нормально.                            -->

<!-- Severity column literals: Low / Medium / High for regular risks; "Open question" for rows
     created by Step-7 `Save as Open Question` resolutions (see references/socratic-loop.md). -->

| Risk / debt | Severity | Mitigation | Owner |
|---|---|---|---|
| <e.g. Outbox lag may reach hours during downstream outage> | Medium | <Alert >10 min, on-call playbook, retry backoff> | <DevOps> |
| <e.g. No event schema versioning in v1> | Medium | <ADR-NNNN planned for v2, graceful handling of unknown fields> | <Backend> |
| Open architectural decision: <decision-headline> | Open question | Resolve before <stage trigger or YYYY-MM-DD>; <inline rationale from Step-7 Save-as-OQ> | <owner> |

**Accepted debt (acceptable in v1, plan to fix later):**
- <e.g. Goal entity is not versioned (immutable) — OK for v1, may need audit versioning in v2>

## 12. Glossary

<!-- 🎯 Навіщо: ⭐ СЛОВНИК ДОМЕНУ, який припиняє суперечки через рік («checkpoint —      -->
<!--           weekly чи biweekly? Quarter — календарний чи фіскальний?»).                -->
<!-- 📋 Що писати: таблиця термін / значення. Бізнес-терміни + технічні вперемішку.       -->
<!--           Один термін може мати дві мови у заголовку: «Goal (Обʼєктив)».              -->
<!-- 📌 Приклад: «Lesson | урок усередині курсу, що складається з блоків (text, video)». -->

| Term | Meaning |
|---|---|
| <e.g. Goal> | <quarterly intent in statement form> |
| <e.g. KR> | <Key Result — measurable target linked to a Goal> |
| <e.g. Checkpoint> | <bi-weekly progress update on a KR> |
