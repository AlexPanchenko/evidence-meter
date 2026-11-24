---
status: Draft
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-24"
feature_size: M
---

# CLI Contract — metric-computation (F1)

Command-line surface for `sad.md` `target_surfaces: [cli]` ([F1 ADR 0001](../adr/0001-entrypoints-serve-f1-through-the-cli-only.md)).
Derived by `/sdlc:api-forge` (scenario A) from [PRD](../PRD.md) §4-§5, [sad.md](../sad.md) §6 flows 1-3 and §8,
[data-model.md](../data-model.md) and [F1 ADR 0007](../adr/0007-shared-return-refusals-as-typed-results.md).
Every command maps to a §4 user story; every exit code maps to an `alt` branch. Field origins and the drift
check are in [api-sync-report.md](api-sync-report.md).

All example values are synthetic. Team ids, definition ids, state names and issue keys from a real
definitions file are shown only in the local Lead's terminal, never in logs (SAD §8 privacy ledger).

## Global flags

| Flag | Short | Type | Description |
|---|---|---|---|
| `--help` | `-h` | bool | Print usage and exit 0. |
| `--version` | | bool | On the top-level command only: print `evidence-meter <version>` and exit 0. |

No `--output` format flag: no PRD criterion or flow asks for machine-readable output in F1.

## Exit codes (all commands)

| Code | Class | Meaning | Origin |
|---|---|---|---|
| 0 | success | Measurement recorded, or matches the earlier one; snapshot stored, or identical to a stored one | flow 1 `alt no measurement` / `else same key, same value`; flow 3 `alt no snapshot with this hash` / `else same hash` |
| 1 | unexpected error | Unhandled error; traceback on stderr, nothing recorded (one transaction) | SAD §8 Transactions |
| 2 | usage error | Bad arguments (argparse), or a malformed definitions file | F1 ADR 0007 ("usage errors") |
| 3 | refusal | Nothing computed or stored; the refusal code on stderr says why | flow 2 every branch; flow 3 `alt file unreadable` |
| 4 | reproducibility defect | Same measurement key, different value or inputs; nothing shown, nothing recorded | flow 1 `else same key, different value or inputs`; PRD AC-03 |

Refusal codes (closed list, F1 ADR 0007): `person_breakdown_refused`, `period_not_closed`,
`definitions_missing`, `definition_retired`, `snapshot_missing`, `unmapped_states`, plus the proposal
`snapshot_invalid` (not yet in the ADR; see the report's Deferrals). Codes are bare snake_case, not
`module.error_name`: deviation by F1 ADR 0007.

## Command: `evidence-meter import`

Store one team's snapshot file for one closed period (SAD flow 3; precondition of AC-07, US-04).

### Usage

```
evidence-meter import <snapshot-file> --team <team> --period <YYYY-MM>
```

### Arguments and flags

| Name | Required | Type | Default | Origin |
|---|---|---|---|---|
| `<snapshot-file>` | yes | path to a JSON file | | flow 3 "import the snapshot file"; F1 ADR 0003 |
| `--team` | yes | string | | flow 3 message; `collection_snapshots.team` |
| `--period` | yes | `YYYY-MM` | | flow 3 message; `collection_snapshots.period`; F1 ADR 0006 |

The file holds issues with their state transitions; only issue key, from state, to state and timestamp are
kept (`collection_issue_transitions` columns, F1 ADR 0004). Person fields are dropped before anything is
stored. Transitions before the period stay: a pass finished in the period can start earlier.

### Output (exit 0, stdout)

```
Imported snapshot for team-alpha, 2026-10: 42 issues, 187 transitions.
snapshot: <sha256>
```

```
Snapshot for team-alpha, 2026-10 is identical to the stored one (<sha256>); nothing stored.
```

### Error output (exit 3, stderr)

```
Refused: snapshot_invalid: the file is unreadable or not a snapshot; nothing stored.
```

`TrackerSnapshotCollected` is dispatched after a new snapshot only, never on the identical case.

## Command: `evidence-meter compute`

Compute one definition for one team and one closed period (US-01, US-02, US-03, US-05, US-06, US-07).

### Usage

```
evidence-meter compute <definition-id> --team <team> --period <YYYY-MM> [--version <N>] [--by team|person]
```

### Arguments and flags

| Name | Required | Type | Default | Origin |
|---|---|---|---|---|
| `<definition-id>` | yes | string | | flow 1 `compute cycle-time`; `computation_measurements.definition_id` |
| `--team` | yes | string | | flow 1 and 2; `computation_measurements.team` |
| `--period` | yes | `YYYY-MM` | | flow 1 and 2; `computation_measurements.period`; F1 ADR 0006 |
| `--version` | no | integer ≥ 1 | the current version | flow 1 `[--version N]`; `computation_measurements.definition_version`; AC-10 |
| `--by` | no | `team` \| `person` | `team` | flow 2 `[--by person]`; SAD §8 capability rule; AC-09 |

`--version` after the subcommand is the definition version; `evidence-meter --version` prints the program
version.

### Checks, in order, all before the first write (SAD §6, F1 ADR 0002)

| # | Check | Refusal code (exit 3) | Reply on stderr | Origin |
|---|---|---|---|---|
| 1 | `--by person` | `person_breakdown_refused` | results are team-level only | AC-09, flow 2 |
| 2 | period not closed (UTC month) | `period_not_closed` | the period must be closed first | AC-06, flow 2 |
| 3 | no definitions file | `definitions_missing` | the definitions file is missing, nothing recorded | AC-05, flow 2 |
| 4 | requested version retired | `definition_retired` | use version `<N>`; version `<M>` measurements unchanged | AC-10, flow 2 |
| 5 | no snapshot for team and period | `snapshot_missing` | run `import` for `<team>`, `<period>` first | AC-07, flow 2 |
| 6 | states the state map does not cover | `unmapped_states` | extend the state map with: `<state>`, `<state>` | AC-04, flow 2 |

Stderr form: `Refused: <code>: <reason>`. A refusal never prints a value or a zero.

### Output (exit 0, stdout)

New measurement (AC-01, AC-02):

```
cycle-time v1 for team-alpha, 2026-10: 3.5
outcome: value
passes counted: 18 · issues excluded: 2
definition: cycle-time v1 (<sha256>)
state map: <sha256>  Doing → started · Done → done · Duplicate → excluded
snapshot: <sha256>
Not yet checked by Evidence Guard.
```

No finished passes (AC-01b): `outcome: no_finished_passes` and the line `no finished passes: the median is
not defined` in place of a value; never `0`.

Re-run with the same key (AC-03): the same lines, then `Matches the earlier measurement; nothing recorded.`

| Output field | Origin |
|---|---|
| value | `computation_measurements.value` (REAL, NULL only with `no_finished_passes`) |
| outcome | `computation_measurements.outcome` (`value` \| `no_finished_passes`, CHECK) |
| passes counted | `computation_measurements.passes_counted` `# stale`: column gone from data-model.md (reconcile run 2); owner decides |
| issues excluded | `computation_measurements.issues_excluded` |
| definition id, version, version hash | `computation_measurements.definition_id`, `definition_version`, `definition_version_hash` |
| state map and its hash | `computation_state_maps.canonical_map`, `state_map_hash` |
| snapshot hash | `computation_measurements.snapshot_hash` |
| "Not yet checked by Evidence Guard." | PRD AC-01 |

Nothing in any output identifies a person (PRD §6.1, AC-02).

### Defect output (exit 4, stderr)

```
Defect: the recomputed measurement for this key differs from the recorded one; nothing shown, nothing recorded.
```

`MetricComputed` is dispatched after a new measurement only.

## Backwards-compat policy

- Additive only: a new optional flag is fine; removing or renaming a flag, a refusal code or an exit code
  meaning is a breaking change and needs a major version bump.
- Flag order is not significant.
