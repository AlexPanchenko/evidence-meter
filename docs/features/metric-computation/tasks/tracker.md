# Tracker — metric-computation

> Status of every task in the epic. `implement-tasks` updates `done` as it commits each task.
> States: `todo` · `in_progress` · `blocked` · `review` · `done`. Estimates: S = 2 h, M = half a day, L = a day.

| # | Task | Layer | Owner | Estimate | Blocked by | Status |
|---|---|---|---|---|---|---|
| [T1](T1-shared-kernel.md) | Add shared Team, Period, Refusal codes, records and event types | domain | capstone owner | M | — | todo |
| [T2](T2-platform-config-db.md) | Add platform config and one-transaction database helper | infra | capstone owner | S | — | todo |
| [T12](T12-close-contract-deferrals.md) | Close the contract deferrals and the SAD doc debt | docs | capstone owner | S | — | todo |
| [T3](T3-computation-domain.md) | Implement passes, median and cycle-time outcome in computation domain | domain | capstone owner | L | T1 | todo |
| [T4](T4-definitions-reader.md) | Read definitions file: versions, retirement, state maps, hashes | app | capstone owner | M | T1, T2 | todo |
| [T5](T5-collection-import.md) | Import a snapshot file into immutable collection tables | app | capstone owner | L | T1, T2, T12 | todo |
| [T7](T7-computation-store.md) | Store measurements and state maps by measurement key | infra | capstone owner | M | T1, T2 | todo |
| [T6](T6-collection-latest-snapshot.md) | Serve the latest snapshot for a team and period | infra | capstone owner | S | T5 | todo |
| [T8](T8-compute-use-case.md) | Compute use case: coverage, key lookup, match or defect, record | app | capstone owner | M | T3, T7 | todo |
| [T9](T9-cli-import.md) | Add the import command and the in-process event dispatcher | ports | capstone owner | S | T5 | todo |
| [T10](T10-cli-compute.md) | Add the compute command with ordered checks and replies | ports | capstone owner | L | T4, T6, T8, T9 | todo |
| [T11](T11-nfr-suite.md) | Add the NFR suite: all-or-nothing, person scan, offline, run time, smoke | tests | capstone owner | M | T10 | todo |

**Total:** 12 tasks, ~6.5 person-days.
