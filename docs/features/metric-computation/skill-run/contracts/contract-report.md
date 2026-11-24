# contract-report — metric-computation

**Verdict:** PASS (with deferrals)
**Run:** 2026-11-24 (run 1, first run, `--out-dir docs/features/metric-computation/skill-run/contracts`, `--depth easy`) · **Scenario:** A
**Sources read:** PRD ✓ · sad.md §6 ✓ · data-model ✓ · refusal ADR ✓ (F1 ADR 0007) · CONTEXT ✓
**Contract:** cli.md, events.md · **Self-check:** `check_contract.py` exit 1 on this folder (the script reads the closed list from `skill-run/adr/`, which an `--out-dir` run does not have; see the run notes); exit 0 on a scratch copy placed next to the feature's `adr/`

Surface: sad.md `target_surfaces: [cli]` → `cli.md`; F1 publishes `TrackerSnapshotCollected` and `MetricComputed`
(SAD §6 event ledger) → `events.md`. No HTTP route, so no `openapi.yaml` and no rules file.

## Field origins

| path | origin | confidence |
|---|---|---|
| global.`--help` | argparse default in `entrypoints/cli.py` | high |
| global.`--version` | existing `entrypoints/cli.py` (`--version`, top-level) | high |
| exit.0 | owner decision (given in the brief) F1; flow 1 `alt no measurement`, `else same key, same value`; flow 3 both inner branches | high |
| exit.1 | owner decision (given in the brief) F1; SAD §8 Transactions | high |
| exit.2 | owner decision (given in the brief) F1; F1 ADR 0007 Neutral ("bad arguments are usage errors"), F1 ADR 0005 | high |
| exit.3 | owner decision (given in the brief) F1; flow 2 every branch; flow 3 `alt file unreadable` | high |
| exit.4 | owner decision (given in the brief) F1; AC-03; flow 1 `else same key, different value` | high |
| import.`<snapshot-file>` | flow 3 "import the snapshot file"; F1 ADR 0003 | high |
| import.`--team` | `collection_snapshots.team`; owner decision (given in the brief) F4 | high |
| import.`--period` | `collection_snapshots.period` (`YYYY-MM`, F1 ADR 0006); owner decision (given in the brief) F4 | high |
| import.refusal.`snapshot_invalid` | flow 3 `alt file unreadable or not the snapshot shape`; owner decision (given in the brief) F2 (proposal) | medium |
| import.out.team | `collection_snapshots.team` | high |
| import.out.period | `collection_snapshots.period` | high |
| import.out.issues | flow 3 "issue and transition counts"; distinct `collection_issue_transitions.issue_key` | high |
| import.out.transitions | flow 3 "issue and transition counts"; rows of `collection_issue_transitions` | high |
| import.out.snapshot_hash | `collection_snapshots.snapshot_hash` | high |
| import.out.imported_or_identical | flow 3 `alt no snapshot with this hash` / `else same team, period and hash` | high |
| compute.`<definition-id>` | `computation_measurements.definition_id`; flow 1 "compute cycle-time"; owner decision (given in the brief) F3 | high |
| compute.`--team` | `computation_measurements.team`; flow 1 and flow 2 messages | high |
| compute.`--period` | `computation_measurements.period` (`YYYY-MM`, F1 ADR 0006); flow 1 and flow 2 messages | high |
| compute.`--version` | `computation_measurements.definition_version`; SAD §8 Capability rule (default current); AC-10 | high |
| compute.`--by` | SAD §8 Capability rule (`team` or `person`); AC-09; default `team` decided by the run (F8) | medium |
| compute.refusal.`person_breakdown_refused` | AC-09; flow 2 `alt breakdown by person`; F1 ADR 0007 | high |
| compute.refusal.`period_not_closed` | AC-06; flow 2 `else period not closed`; F1 ADR 0007 | high |
| compute.refusal.`definitions_missing` | AC-05; flow 2 `else definitions file absent`; F1 ADR 0007 | high |
| compute.refusal.`definition_retired` | AC-10; flow 2 `else requested version retired`; F1 ADR 0007 | high |
| compute.refusal.`snapshot_missing` | AC-07; flow 2 `else no snapshot`; F1 ADR 0007 | high |
| compute.refusal.`unmapped_states` | AC-04; flow 2 `else states the state map does not cover`; F1 ADR 0007 | high |
| compute.defect.reproducibility | AC-03; flow 1 `else same key, different value`; F1 ADR 0008 | high |
| compute.usage.definitions_content | F1 ADR 0005, F1 ADR 0007; decided by the run (F7) | medium |
| compute.out.definition_id | `computation_measurements.definition_id`; AC-02 | high |
| compute.out.definition_version | `computation_measurements.definition_version`; AC-02 | high |
| compute.out.team | `computation_measurements.team` | high |
| compute.out.period | `computation_measurements.period` | high |
| compute.out.outcome | `computation_measurements.outcome` (CHECK); F1 ADR 0009; AC-01b | high |
| compute.out.value | `computation_measurements.value` (REAL, NULL only with `no_finished_passes`); AC-01 | high |
| compute.out.passes_counted | `computation_measurements.passes_counted`; AC-02 | high |
| compute.out.issues_excluded | `computation_measurements.issues_excluded`; AC-02 | high |
| compute.out.state_map | `computation_state_maps.canonical_map`; AC-02 | high |
| compute.out.state_map_hash | `computation_measurements.state_map_hash` | high |
| compute.out.snapshot | `computation_measurements.snapshot_hash`; AC-03 | high |
| compute.out.not_yet_checked | AC-01; flow 1 reply | high |
| compute.out.recorded_or_matches | flow 1 `alt no measurement` / `else same key, same value`; AC-03 | high |
| event.TrackerSnapshotCollected.team | `collection_snapshots.team`; SAD §8 privacy ledger "Events in memory" | medium |
| event.TrackerSnapshotCollected.period | `collection_snapshots.period` | medium |
| event.TrackerSnapshotCollected.snapshot_hash | `collection_snapshots.snapshot_hash` | medium |
| event.MetricComputed.team | `computation_measurements.team`; SAD §8 privacy ledger "Events in memory" | medium |
| event.MetricComputed.period | `computation_measurements.period` | medium |
| event.MetricComputed.definition_id | `computation_measurements.definition_id`; SAD §8 privacy ledger "Events in memory" | medium |
| event.MetricComputed.definition_version | `computation_measurements.definition_version` | medium |
| event.MetricComputed.definition_version_hash | `computation_measurements.definition_version_hash` | medium |
| event.MetricComputed.snapshot_hash | `computation_measurements.snapshot_hash` | medium |
| event.MetricComputed.state_map_hash | `computation_measurements.state_map_hash` | medium |
| event.MetricComputed.outcome | `computation_measurements.outcome`; F1 ADR 0009 ("`MetricComputed` carries the same pair") | high |
| event.MetricComputed.value | `computation_measurements.value`; F1 ADR 0009 | high |
| event.MetricComputed.passes_counted | `computation_measurements.passes_counted` | medium |
| event.MetricComputed.issues_excluded | `computation_measurements.issues_excluded` | medium |

57 fields. Dropped for lack of an origin: none of the template rows lacked an origin; the template's
placeholder `<flag>` rows were replaced, not kept. No idempotency key, retry or pagination field (CLI only).

## Drift check

1. Command ↔ data-model *(core)* — ✓ `import` writes `collection_snapshots`, `collection_issue_transitions`;
   `compute` reads `collection_*` and writes `computation_measurements`, `computation_state_maps`.
2. Refusal code ↔ ADR closed list *(core)* — ✓ the six codes in cli.md equal the `Codes:` line parsed from
   `adr/0007-shared-return-refusals-as-typed-results.md`; `snapshot_invalid` is a proposal and a Deferral.
3. Constraint ↔ column *(core)* — ✓ `--period` `YYYY-MM` ↔ `period TEXT` (F1 ADR 0006); `--version` integer ↔
   `definition_version INTEGER`; `outcome` ↔ CHECK (`value`, `no_finished_passes`); `value` absent only with
   `no_finished_passes` ↔ CHECK; `--team` text ↔ `team TEXT`.
4. Coverage *(supporting)* — ✓ (deferred: KPI 3 refused-run counts) every table surfaced (`collection_issue_transitions`
   through the import counts, `computation_state_maps` through the shown state map); AC-01..AC-10 and AC-01b
   each have a reply; `compute` serves US-01..US-07, `import` serves the AC-07 precondition (F1 ADR 0003).
5. Flow branches *(supporting)* — ✓ (deferred: F7) every `alt`/`else` of flows 1-3 has an exit code; the exit-2
   reply for definitions-file content (F7) has no §6 branch: a sequence gap.
6. Privacy *(core)* — ✓ no output field, flag or example names or counts a person; `--by person` is a refusal
   row; examples use `team-alpha`, `team-beta`, `cycle-time`, invented states. Private names (team id,
   definition id, state names) appear only in the local terminal reply and in-process events (F6).

## Owner decisions

| Flag | Action | Result |
|---|---|---|
| F1. CLI exit codes | owner decision (given in the brief): the skill's class scheme 0-4 | exit-code table in cli.md |
| F2. Flow 3 import error (unreadable or malformed snapshot file) has no AC or ADR code | owner decision (given in the brief): Save as OQ; proposed code `snapshot_invalid`, exit 3 | proposal row and Deferral |
| F3. Positional argument of `compute` | owner decision (given in the brief): the definition id | `evidence-meter compute <definition-id>` |
| F4. How `import` names the team and period | owner decision (given in the brief): `--team` and `--period` flags | import usage |
| F5. Does `import` refuse a period that is not closed? (SAD §6 flag, data-model "Flags for the build") | decided by the run, owner to confirm: Save as OQ; no refusal at import, because no AC or ADR code covers it and the rule forbids inventing one; `compute` still refuses (AC-06) | import accepts any `YYYY-MM`; Deferral |
| F6. SAD §8 Logging says stderr never carries a team id, definition id or state name, and the privacy ledger's "Terminal reply" row lists state names and the state map only; yet AC-02 shows the definition id, AC-04 lists unmapped states, AC-07 names the team, and the skill puts refusals on stderr | decided by the run, owner to confirm: Fix the source first (SAD §8); the contract treats the stdout result and the stderr refusal line as the terminal reply to the local Lead, and no log record carries those names | note in cli.md; Deferral |
| F7. A definitions file without the named definition id, version or a state map for the team has no AC and no §6 branch | decided by the run, owner to confirm: usage error, exit 2, per F1 ADR 0007 ("a malformed definitions file or bad arguments are usage errors") and F1 ADR 0005 | check 3a in cli.md; Deferral (sequence gap) |
| F8. `--by` has values (SAD §8) but no stated default | decided by the run, owner to confirm: default `team`, the only value that computes | cli.md flag row |
| F9. Event payload fields are not listed in the SAD or bc-map | decided by the run, owner to confirm: Accept as is; fields mirror the recorded row (F1 ADR 0002 publishes after the insert; F1 ADR 0009 names outcome and value) | events.md; medium-confidence origins |
| F10. Top-level `--version` (program version, existing cli.py) and `compute --version N` (definition version, SAD §8) share a name | decided by the run, owner to confirm: Accept as is; argparse keeps them apart per parser, the global-flags row says "top-level only" | cli.md global flags note |

## Unresolved origins

- `event.*` fields other than outcome and value · origin is the table column, not a named payload in SAD or
  bc-map · `--reconcile` tightens once the SAD or `shared/events.py` names the payload (F9).
- `compute.--by` default · decided by the run (F8) · tightens when SAD §8 states the default.

## Tests the contract implies

- Exit-class tests: one per class 0, 1, 2, 3, 4 on `compute`, and 0 (new and identical), 2, 3 on `import`.
- `compute` order: `--by person` with no definitions file and an open period → `person_breakdown_refused`
  (check 1 before 2 and 3); open period with no definitions file → `period_not_closed` (2 before 3);
  no definitions file and no snapshot → `definitions_missing` (3 before 5); retired version and no snapshot →
  `definition_retired` (4 before 5); no snapshot and an incomplete state map → `snapshot_missing` (5 before 6);
  unmapped states → `unmapped_states` listing every unmapped state.
- `compute` check 3a: a definitions file without the definition id, the version or the team's state map → exit 2.
- `compute` check 7: a stored row with the same key and a different value → exit 4, no value on stdout,
  store unchanged.
- Every exit 2, 3 and 4 leaves the store row counts unchanged (all-or-nothing) and publishes no event.
- `import` check 2: an unreadable file and a JSON file of the wrong shape → `snapshot_invalid`, nothing stored.
- `import` identical re-import → exit 0, "identical", no new row, no `TrackerSnapshotCollected`.
- Privacy: every stdout and stderr line of every command and every log record holds no person field; no log
  record holds a team id, definition id, state name or issue key.

## Deferrals

| What | Why parked | Next step |
|---|---|---|
| `snapshot_invalid` (proposal, exit 3) for flow 3 `alt file unreadable or not the snapshot shape` | no AC or ADR code covers it (owner decision F2) | add it to F1 ADR 0007 `Codes:` and a PRD AC, then `--reconcile` |
| F5: import of a period that is not closed | no AC or ADR rule; inventing a code is forbidden | owner decides in the SAD or PRD; `--reconcile` |
| F6: SAD §8 Logging and privacy ledger vs replies that name the team, definition id and states | the source contradicts AC-02, AC-04, AC-07 | fix SAD §8 (terminal reply vs log record), then `--reconcile` |
| F7: definitions-file content errors (missing definition id, version or team state map) | no §6 branch; exit 2 by ADR 0005/0007 reading | add a branch to SAD §6 flow 2, then `--reconcile` |
| KPI 3: share of runs refused for unmapped states | AC-04 records nothing; SAD §11 open question | resolve at `/sdlc:break-tasks`; the contract adds no counter or log |
