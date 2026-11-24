# Expand → backfill → contract on SQLite

Three migrations, three commits, three releases. Example: a NOT NULL column `<col>` on `<table>`.

## 1. Expand: `NNNN_expand_add_<col>_to_<table>`

```sql
-- up: add nullable; from this release the app writes <col> on every new row.
ALTER TABLE <table> ADD COLUMN <col> TEXT;
```

```sql
-- down (SQLite 3.35+; fails if <col> is indexed or in a constraint: drop those first)
ALTER TABLE <table> DROP COLUMN <col>;
```

## 2. Backfill: `NNNN_backfill_<col>_on_<table>` + `backfill-<col>.md`

```sql
-- up: resumable, touches only rows still missing a value.
UPDATE <table> SET <col> = <value or expression> WHERE <col> IS NULL;
```

```sql
-- down: back to the state after expand. Lossy: also nulls rows the app wrote after expand.
UPDATE <table> SET <col> = NULL;
```

The companion note gives: rows affected, time in one transaction, why no batching is needed (or the
batch size and cursor if it is), and what the down loses.

## 3. Contract: `NNNN_contract_<col>_not_null_on_<table>`

SQLite has no `ALTER COLUMN ... SET NOT NULL`. Rebuild (SQLite's 12-step procedure, with
`foreign_keys` off, which is the runner's connection default):

```sql
-- up
CREATE TABLE <table>_new (
    id INTEGER PRIMARY KEY,
    <every existing column, same types and constraints>,
    <col> TEXT NOT NULL,
    UNIQUE (<natural key>)
) STRICT;
INSERT INTO <table>_new (id, <columns>, <col>) SELECT id, <columns>, <col> FROM <table>;
DROP TABLE <table>;
ALTER TABLE <table>_new RENAME TO <table>;
CREATE INDEX IF NOT EXISTS <each index of the old table> ON <table> (...);
```

```sql
-- down: the same rebuild with <col> nullable.
```

- Ids are copied, so child tables' `REFERENCES <table> (id)` still match.
- After `RENAME`, SQLite stores the table's SQL with a quoted name; compare structure (`pragma
  table_info`, `index_list`, `foreign_key_list`), not SQL text. `roundtrip.py` does.
- A rename of a column is the same three steps with a new column, a copy in the backfill and the old
  column dropped in the contract rebuild.
