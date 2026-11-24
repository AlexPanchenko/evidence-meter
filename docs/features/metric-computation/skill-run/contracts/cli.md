---
status: Draft
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-24"
feature_size: M
---

# CLI Contract — metric-computation

Derived from PRD §4-§5, sad.md §6 and §8, data-model.md and the refusal ADR
([F1 ADR 0007](../../adr/0007-shared-return-refusals-as-typed-results.md)). Origins and drift check:
[contract-report.md](contract-report.md). Events: [events.md](events.md).

## Global flags

| Flag | Short | Type | Description |
|---|---|---|---|
| `--help` | `-h` | bool | Print usage and exit 0. |
| `--version` | | bool | Top-level only: print the program version and exit 0. On `compute`, `--version N` is the definition version (below). |

## Exit codes (all commands)

| Code | Class | Meaning | Origin |
|---|---|---|---|
| 0 | success | a new snapshot or measurement recorded, or an idempotent no-op (identical re-import, matching re-run) | flow 1 `alt no measurement` / `else same key, same value`; flow 3 `alt no snapshot` / `else same hash` |
| 1 | unexpected error | traceback on stderr, nothing recorded | SAD §8 Transactions |
| 2 | usage error | bad arguments (argparse), a malformed definitions file, a definition id or version number the file does not have, a team with no state map in the file; nothing recorded | F1 ADR 0007 Neutral, F1 ADR 0005 Negative |
| 3 | refusal | nothing recorded; `Refused: <code>: <reason>` on stderr | flow 2 every branch; flow 3 `alt file unreadable` |
| 4 | defect | a re-run with the same key gave a different outcome or value; no value shown, nothing recorded | AC-03, flow 1 `else same key, different value` |

Refusal codes (closed list, F1 ADR 0007): `person_breakdown_refused`, `period_not_closed`,
`definitions_missing`, `definition_retired`, `snapshot_missing`, `unmapped_states`. Proposals not yet in the
ADR: `snapshot_invalid` (Deferral, see the report).

The refusal or defect line on stderr is the terminal reply to the local Lead, not a log record; no log record
carries a team id, a definition id, a state name or an issue key (SAD §8 Logging; see report, flag F6).

## Command: `evidence-meter import`

Precondition of AC-07: store one team's snapshot file for one closed period so `compute` can read it
(F1 ADR 0003, flow 3).

### Usage

```
evidence-meter import <snapshot-file> --team <team> --period <YYYY-MM>
```

### Arguments and flags

| Name | Required | Type | Default | Origin |
|---|---|---|---|---|
| `<snapshot-file>` | yes | path to a JSON file | | flow 3 "import the snapshot file", F1 ADR 0003 |
| `--team` | yes | text, team id | | `collection_snapshots.team`; owner decision (given in the brief) |
| `--period` | yes | `YYYY-MM` (UTC month) | | `collection_snapshots.period`, F1 ADR 0006; owner decision (given in the brief) |

A period that is not closed yet is accepted at import (report flag F5); `compute` refuses it (AC-06).

### Checks, in order, all before the first write

| # | Check | Refusal code (exit 3) | Reply on stderr | Origin |
|---|---|---|---|---|
| 1 | arguments parse; `--period` matches `YYYY-MM` | none, exit 2 | argparse usage line | class scheme, column format |
| 2 | file readable and in the snapshot shape | `snapshot_invalid` (proposal) | `Refused: snapshot_invalid: the snapshot file cannot be read or is not a snapshot; nothing stored` | flow 3 `alt file unreadable or not the snapshot shape`; owner decision (given in the brief) |
| 3 | same team, period and hash already stored | none, exit 0 | (stdout) identical, nothing stored | flow 3 `else same team, period and hash` |

Person fields in the file are dropped before the hash and never stored, shown or logged (F1 ADR 0004).

### Output (exit 0, stdout)

New snapshot:

```
imported snapshot: team-alpha 2026-10
issues: 40
transitions: 112
snapshot hash: <sha256>
```

Identical re-import (no event published):

```
identical to the stored snapshot: team-alpha 2026-10, snapshot hash <sha256>; nothing stored
```

Refusal (exit 3, stderr):

```
Refused: snapshot_invalid: the snapshot file cannot be read or is not a snapshot; nothing stored
```

Unexpected error (exit 1, stderr): a traceback; nothing stored.

| Output field | Origin |
|---|---|
| team | `collection_snapshots.team` |
| period | `collection_snapshots.period` |
| issues | flow 3 "new snapshot with issue and transition counts" (distinct `collection_issue_transitions.issue_key`) |
| transitions | flow 3 "new snapshot with issue and transition counts" (rows of `collection_issue_transitions`) |
| snapshot hash | `collection_snapshots.snapshot_hash` |
| imported / identical | flow 3 `alt no snapshot with this hash` / `else same team, period and hash` |

Nothing in any output identifies a person.

## Command: `evidence-meter compute`

US-01..US-07: compute one metric (cycle time) for one team and one closed period, show what made it, match
a re-run, refuse with a plain reason.

### Usage

```
evidence-meter compute <definition-id> --team <team> --period <YYYY-MM> [--version N] [--by team|person]
```

### Arguments and flags

| Name | Required | Type | Default | Origin |
|---|---|---|---|---|
| `<definition-id>` | yes | text, a definition id from the definitions file (`cycle-time`) | | `computation_measurements.definition_id`; flow 1 "compute cycle-time"; owner decision (given in the brief) |
| `--team` | yes | text, team id | | `computation_measurements.team`; flow 1 message |
| `--period` | yes | `YYYY-MM` (UTC month) | | `computation_measurements.period`, F1 ADR 0006; flow 1 message |
| `--version` | no | integer, definition version number | the current published version | `computation_measurements.definition_version`; SAD §8 Capability rule; AC-10 |
| `--by` | no | `team` or `person` | `team` | SAD §8 Capability rule; AC-09; default: report flag F8 |

### Checks, in order, all before the first write

| # | Check | Refusal code (exit 3) | Reply on stderr | Origin |
|---|---|---|---|---|
| 0 | arguments parse; `--period` is `YYYY-MM`, `--version` an integer, `--by` one of `team`, `person` | none, exit 2 | argparse usage line | class scheme, column types |
| 1 | `--by person` (no I/O) | `person_breakdown_refused` | `Refused: person_breakdown_refused: results are team-level only` | AC-09, flow 2 `alt breakdown by person` |
| 2 | period closed in UTC (pure, clock injected) | `period_not_closed` | `Refused: period_not_closed: the period must be closed first` | AC-06, flow 2 `else period not closed`, F1 ADR 0006 |
| 3 | definitions file present | `definitions_missing` | `Refused: definitions_missing: the definitions file is missing; nothing recorded` | AC-05, flow 2 `else definitions file absent` |
| 3a | definitions file parses; it has the definition id, the version and a state map for the team | none, exit 2 | `Usage error: <what is wrong in the definitions file or arguments>` | F1 ADR 0005, F1 ADR 0007; report flag F7 |
| 4 | requested version not retired | `definition_retired` | `Refused: definition_retired: version 1 is retired; use version 2. Version 1 measurements are unchanged` | AC-10, flow 2 `else requested version retired` |
| 5 | a stored snapshot for team and period | `snapshot_missing` | `Refused: snapshot_missing: run import for team-beta 2026-10 first` | AC-07, flow 2 `else no snapshot` |
| 6 | the state map covers every state in the snapshot | `unmapped_states` | `Refused: unmapped_states: extend the state map with: Review, Blocked` | AC-04, flow 2 `else states the state map does not cover` |
| 7 | same key already recorded with a different outcome or value | none, exit 4 | `Defect: reproducibility: the same inputs gave a different result; no value shown, nothing recorded` | AC-03, flow 1 `else same key, different value`, F1 ADR 0008 |

Checks 1-2 read nothing; 3-4 read the definitions file only; 5 reads `collection_*`; 6-7 run after the formula
and before the insert. A test can check that `--by person` refuses before the definitions file is opened.

### Output (exit 0, stdout)

New measurement:

```
cycle-time version 1 · team-alpha · 2026-10
outcome: value
value: 4.5 days (median of passes finished in 2026-10)
passes counted: 12
issues excluded: 2
state map: Doing → started, Done → done, Dropped → excluded (<sha256>)
snapshot: <sha256>
not yet checked by Evidence Guard
recorded: new measurement
```

No finished passes (AC-01b, a result, not a refusal; no number, no zero):

```
cycle-time version 1 · team-alpha · 2026-10
outcome: no_finished_passes (no passes finished in 2026-10; the median is not defined)
passes counted: 0
issues excluded: 3
state map: Doing → started, Done → done, Dropped → excluded (<sha256>)
snapshot: <sha256>
not yet checked by Evidence Guard
recorded: new measurement
```

Matching re-run (AC-03, nothing recorded, no event): the same lines, with the last line
`matches the earlier measurement; nothing recorded`.

Refusal (exit 3, stderr), for example:

```
Refused: unmapped_states: extend the state map with: Review, Blocked
```

Defect (exit 4, stderr):

```
Defect: reproducibility: the same inputs gave a different result; no value shown, nothing recorded
```

| Output field | Origin |
|---|---|
| definition id | `computation_measurements.definition_id`; AC-02 |
| definition version | `computation_measurements.definition_version`; AC-02 |
| team | `computation_measurements.team` |
| period | `computation_measurements.period` |
| outcome | `computation_measurements.outcome` (CHECK: `value`, `no_finished_passes`); F1 ADR 0009 |
| value | `computation_measurements.value`, in the definition's unit; absent with `no_finished_passes`; AC-01 |
| passes counted | `computation_measurements.passes_counted`; AC-02 |
| issues excluded | `computation_measurements.issues_excluded`; AC-02 |
| state map | `computation_state_maps.canonical_map`; AC-02 |
| state map hash | `computation_measurements.state_map_hash` |
| snapshot | `computation_measurements.snapshot_hash`; AC-03 "same snapshot" |
| not yet checked by Evidence Guard | AC-01 |
| recorded / matches | flow 1 `alt no measurement` / `else same key, same value`; AC-03 |

Nothing in any output identifies a person. A breakdown by person is refused (`person_breakdown_refused`);
there is no option that shows one.

## Backwards-compat policy

Additive only. Removing or renaming a flag, a refusal code or an exit-code meaning is breaking.
