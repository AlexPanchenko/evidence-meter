---
status: Draft
owner: "capstone owner"
reviewers: ["implementing engineer", "Tech Lead"]
updated_at: "2026-11-24"
feature_size: "M"
---

# Test plan — metric-computation (F1)

A Lead names one team and one closed period and gets the team's cycle time, traced to its definition
version, state map and inputs, or a plain refusal; nothing per person, nothing partial. Sources:
[PRD](PRD.md) §5-§6, [sad.md](sad.md) §6 and §10, [data-model.md](data-model.md),
[contracts/cli.md](contracts/cli.md). Expected values in golden data are computed by hand (AGENTS.md).

## Levels

| Level | Scope | Strategy |
|---|---|---|
| Unit | Computation `domain`: passes from transitions, median, period rule, state-map coverage | In memory, no I/O; golden data with hand-computed values |
| Integration | A context against the store and files it owns: snapshot store, measurement store, definitions file reader | A real temporary database file built by the project's migration runner per test; real temporary files; no mocked store |
| Contract | The CLI surface in `contracts/cli.md` (exit-code classes, refusal codes, output fields) and the event payloads | The real command output checked against the contract tables; every output scanned for person fields |
| E2E | `import` and `compute` through the command entry point | The entry point called in process with an argument list (stdout, stderr and exit code captured) against a temporary store and definitions file; one smoke test runs the installed command |
| Load | PRD §6 run time | Timed run on a generated 5,000-issue snapshot |

<!-- N/A: component, visual-regression, e2e-through-UI — target_surfaces is [cli], no UI surface. -->

## AC coverage

| AC (PRD.md §5) | Test name (intent-based) | Level | Expected outcome |
|---|---|---|---|
| AC-01 happy path | cycle time is the median of passes finished in the period | unit | golden snapshot gives the hand-computed median |
| AC-01 | compute records the measurement and marks it not yet checked | e2e | success; one measurement stored; reply says not yet checked by Evidence Guard |
| AC-01b no finished passes | no finished passes gives no value, never zero | unit | outcome "no finished passes", no value |
| AC-01b | a no-value measurement is stored without a value | integration | stored with outcome "no finished passes" and an empty value; the store rejects a value with that outcome |
| AC-02 traceability | the reply names definition, version, state map, passes and exclusions | e2e | all five appear in the reply, nothing that identifies a person |
| AC-02 | compute output matches the contract's output fields | contract | every output field is one listed in `cli.md`; no other field |
| AC-03 reproducibility | a re-run with the same inputs matches and records nothing | integration | same key found; no second row; same value and inputs returned |
| AC-03 | a different result for the same key is a defect | integration | defect reported; no value returned; nothing stored |
| AC-03 | re-run and defect replies through the command | e2e | match: success and "matches the earlier measurement"; defect: defect exit class, no value shown |
| AC-04 unmapped states | coverage check lists every unmapped state | unit | the exact set of uncovered states, nothing computed |
| AC-04 | unmapped states are refused and nothing is stored | e2e | refusal exit class; the states are listed; store unchanged |
| AC-05 definitions file missing | the definitions reader reports an absent file as a refusal, not an error | integration | refusal "definitions missing" returned; nothing raised |
| AC-05 | a missing definitions file is refused | e2e | refusal exit class; message names the missing file; store unchanged |
| AC-06 period not closed | a period is closed only after its UTC month ends | unit | last second of the month: open; first second of the next: closed |
| AC-06 | an open period is refused before any read | e2e | refusal exit class; "close the period first"; store unchanged |
| AC-07 no snapshot | the latest snapshot lookup finds none for team and period | integration | no snapshot returned for an empty store or another team's snapshot |
| AC-07 | a missing snapshot is refused with "import first", never zero | e2e | refusal exit class; the reply names import for the team and period; no value |
| AC-08 reopened work | a reopen starts a new pass, counted in the month of its own done | unit | golden issue done 2026-09, reopened and done 2026-10: one pass in each month, the second from the reopen |
| AC-08 | an earlier month's measurement is unchanged by a later compute | integration | the 2026-09 row is byte-identical before and after computing 2026-10 |
| AC-09 person breakdown | a breakdown by person is refused before anything is read | e2e | refusal exit class; the definitions file and store are not opened; nothing stored or logged |
| AC-09 | no output carries a person field | contract | a scan of stdout, stderr, stored rows and log lines finds no person field |
| AC-10 retired version | a retired version is refused and the current one named | integration | the definitions reader marks version 1 retired and names version 2 |
| AC-10 | a retired version leaves old measurements untouched | e2e | refusal exit class; version 2 named; version 1 rows unchanged and still name version 1 |

Coverage: 11/11 ACs, 23 tests, at least 2 per AC; every error and authorization AC has its own rows.

## Edge cases / error paths

- Identical snapshot imported twice → nothing stored the second time, no event, success.
- A different file for the same team and period → a new snapshot; compute uses the latest; older measurements still point at the older snapshot.
- Snapshot file unreadable or not a snapshot → refused as an invalid snapshot, nothing stored (proposal, see the contract report Deferrals).
- Person fields in a snapshot file → dropped at import; no stored column, reply or log line carries them.
- Malformed definitions file → usage error class, nothing recorded.
- Period not in `YYYY-MM` form, or `--version 0` → usage error class.
- Two passes with equal timestamps → order follows the stored transition order (tie-break), result stable across re-runs.
- An even number of passes → median is the mean of the two middle durations (golden value by hand).
- Excluded issues (won't do, duplicate) → counted as excluded, never as passes.

## Test data

- Seed strategy: small JSON snapshot fixtures for `team-alpha` and `team-beta` with issues `PRJ-DEMO-1..n` and states `Open`, `Doing`, `Done`, `Duplicate`; a synthetic TOML definitions file with `cycle-time` versions 1 (retired) and 2; each golden fixture carries its expected values computed by hand in a comment.
- Integration dependency: a real temporary database file per test, created by the project's migration runner; real temporary files for snapshots and definitions; no mocked store.
- Cleanup boundary: per test (temporary directory removed); no test shares a database file.
- Synthetic only: no real team, state, definition code or person name in any fixture.

## NFR validation

- Run time: one team and period with a generated 5,000-issue snapshot → compute finishes in ≤ 10 s; the test fails above that. Runs on every PR in the default check.
- Reproducibility: covered by AC-03 rows over the golden data.
- Offline: compute runs with network access blocked → it finishes with no network attempt (integration).
- Per-person data: covered by the AC-09 contract row (stdout, stderr, stored rows, logs).
- All-or-nothing: one parametrised e2e walks every refusal (AC-04..AC-07, AC-09, AC-10) and the AC-03 defect → the store is byte-identical before and after each.

## CI placement

- On every PR, in the default check: unit, integration, contract, e2e in process, the timed run-time test.
- The installed-command smoke test also runs on every PR (one test, under a second).
- Nothing is scheduled-only: the whole feature runs locally against files.

## Edits log

- Owner accepted the AC→level map as proposed (23 tests, 11/11 ACs; AC-05 integration row added after the count check).
- E2E through the entry point in process plus one installed-command smoke test (owner choice).
- Run-time test on every PR in the default check (owner choice, SAD QG-4).
