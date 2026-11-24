-- Collection: an immutable snapshot per team, period and hash, and its issue transitions
-- (F1 ADR 0003, 0004). Person fields never reach these tables. Timestamps: ISO 8601 UTC 'Z', app-set.
CREATE TABLE IF NOT EXISTS collection_snapshots (
    id INTEGER PRIMARY KEY,
    team TEXT NOT NULL,
    period TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    UNIQUE (team, period, snapshot_hash)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_collection_snapshots_latest
    ON collection_snapshots (team, period, imported_at);

CREATE TABLE IF NOT EXISTS collection_issue_transitions (
    id INTEGER PRIMARY KEY,
    snapshot_id INTEGER NOT NULL REFERENCES collection_snapshots (id),
    issue_key TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT NOT NULL,
    transitioned_at TEXT NOT NULL
) STRICT;

CREATE INDEX IF NOT EXISTS idx_collection_issue_transitions_snapshot
    ON collection_issue_transitions (snapshot_id, issue_key, transitioned_at);
