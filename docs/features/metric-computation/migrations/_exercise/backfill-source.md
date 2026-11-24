# Backfill: `collection_snapshots.source`

Exercise for the m06-l05 hard level (expand → backfill → contract). Not promoted to `migrations/`: F1
does not need the column. The plausible need: a second Collection adapter (tracker API) writes into the
same tables (F1 ADR 0003), so a snapshot should say where it came from.

| Phase | Migration | App release | Reversible by |
|---|---|---|---|
| Expand | `0004_expand_add_source_to_collection_snapshots` | import writes `source = 'file'` on every new snapshot | `DROP COLUMN` (SQLite 3.35+) |
| Backfill | `0005_backfill_source_on_collection_snapshots` | none | `UPDATE ... SET source = NULL` |
| Contract | `0006_contract_source_not_null_on_collection_snapshots` | readers may rely on `source` | table rebuild to nullable |

- **Size and time:** one row per import; a Lead's file holds tens to hundreds of snapshots, so one
  `UPDATE` in the runner's transaction takes well under a second. No batching or cursor needed.
- **Resumable:** the `WHERE source IS NULL` makes a re-run touch only rows still missing a value.
- **Down of the backfill is lossy:** it nulls every row, including rows the app wrote after expand.
  That is the state the expand step can drop; it is wrong only if you stop between backfill-down and
  expand-down, which nobody does on purpose.
- **Contract on SQLite:** a rebuild, not `SET NOT NULL`. `collection_issue_transitions` keeps its
  `REFERENCES collection_snapshots (id)` because ids are copied and the new table takes the old name.
  Run it with `foreign_keys` off (the runner's default).
