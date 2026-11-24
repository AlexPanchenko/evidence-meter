-- Collection: immutable imported snapshots and their issue transitions (F1 ADR 0003, 0004, 0006).
-- Natural key of a snapshot: team, period and SHA-256 of the canonical form (SAD §8 ID strategy).
CREATE TABLE IF NOT EXISTS collection_snapshots (
    id INTEGER PRIMARY KEY,
    team_id TEXT NOT NULL,
    period TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    UNIQUE (team_id, period, snapshot_hash)
) STRICT;

CREATE TABLE IF NOT EXISTS collection_issue_transitions (
    id INTEGER PRIMARY KEY,
    snapshot_id INTEGER NOT NULL REFERENCES collection_snapshots (id),
    issue_key TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT NOT NULL,
    transitioned_at TEXT NOT NULL
) STRICT;

-- Serves the foreign key and "read collection_*" (transitions of one snapshot, per issue in time order).
CREATE INDEX IF NOT EXISTS idx_collection_issue_transitions_snapshot
    ON collection_issue_transitions (snapshot_id, issue_key, transitioned_at);
