-- Exercise, step 3 of 3, contract: SQLite has no ALTER COLUMN SET NOT NULL, so rebuild the table
-- (SQLite's 12-step procedure; the runner's connection has foreign_keys off).
CREATE TABLE collection_snapshots_new (
    id INTEGER PRIMARY KEY,
    team TEXT NOT NULL,
    period TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    source TEXT NOT NULL,
    UNIQUE (team, period, snapshot_hash)
) STRICT;
INSERT INTO collection_snapshots_new (id, team, period, snapshot_hash, imported_at, source)
    SELECT id, team, period, snapshot_hash, imported_at, source FROM collection_snapshots;
DROP TABLE collection_snapshots;
ALTER TABLE collection_snapshots_new RENAME TO collection_snapshots;
CREATE INDEX IF NOT EXISTS idx_collection_snapshots_latest
    ON collection_snapshots (team, period, imported_at);
