---
status: Draft
owner: "capstone owner"
reviewers: []
updated_at: "2026-11-24"
feature_size: M
---

# Events — metric-computation

In-process only: types in `shared/events.py`, dispatched by `entrypoints/` (F1 ADR 0002). Names from
[docs/bc-map.md](../../../../bc-map.md). Origins: [contract-report.md](contract-report.md).

| Event (bc-map name) | Published by | When | Not published when | Listeners now |
|---|---|---|---|---|
| `TrackerSnapshotCollected` | Collection, `import` | flow 3, after the snapshot and its transitions are inserted | identical re-import; `snapshot_invalid`; any error | none yet (Computation does not consume it in F1, SAD §11) |
| `MetricComputed` | Computation, `compute` | flow 1 `alt no measurement with this key`, after the insert | matching re-run; every refusal; the reproducibility defect | none yet (Evidence Guard, later) |

Not published in F1 (SAD §6 event ledger, §11 accepted debt): `GitHistoryCollected`, `CollectionFailed`,
`DefinitionVersionPublished`, `DefinitionVersionRetired`, `ReportingPeriodClosed`.

## `TrackerSnapshotCollected`

| Field | Type | Origin | Private name? |
|---|---|---|---|
| `team` | text | `collection_snapshots.team` | yes: in process only, never logged |
| `period` | text `YYYY-MM` | `collection_snapshots.period` | no |
| `snapshot_hash` | text, SHA-256 hex | `collection_snapshots.snapshot_hash` | no |

## `MetricComputed`

| Field | Type | Origin | Private name? |
|---|---|---|---|
| `team` | text | `computation_measurements.team` | yes: in process only, never logged |
| `period` | text `YYYY-MM` | `computation_measurements.period` | no |
| `definition_id` | text | `computation_measurements.definition_id` | yes: in process only, never logged |
| `definition_version` | integer | `computation_measurements.definition_version` | no |
| `definition_version_hash` | text, SHA-256 hex | `computation_measurements.definition_version_hash` | no |
| `snapshot_hash` | text, SHA-256 hex | `computation_measurements.snapshot_hash` | no |
| `state_map_hash` | text, SHA-256 hex | `computation_measurements.state_map_hash` | no |
| `outcome` | `value` or `no_finished_passes` | `computation_measurements.outcome`, F1 ADR 0009 | no |
| `value` | real or null (null only with `no_finished_passes`) | `computation_measurements.value`, F1 ADR 0009 | no |
| `passes_counted` | integer | `computation_measurements.passes_counted` | no |
| `issues_excluded` | integer | `computation_measurements.issues_excluded` | no |

- Payload holds no person field and is never written or logged (SAD §8 privacy ledger).
- Additive only: a new field is fine; a rename is a new event name in bc-map.
