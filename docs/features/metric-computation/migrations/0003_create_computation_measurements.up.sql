-- Computation: each state map used, by hash, and measurements keyed by every input (F1 ADR 0008, 0009).
-- snapshot_hash points at Collection's snapshot without a foreign key: no FK crosses a context.
CREATE TABLE IF NOT EXISTS computation_state_maps (
    id INTEGER PRIMARY KEY,
    state_map_hash TEXT NOT NULL UNIQUE,
    canonical_map TEXT NOT NULL,
    recorded_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS computation_measurements (
    id INTEGER PRIMARY KEY,
    team TEXT NOT NULL,
    period TEXT NOT NULL,
    definition_id TEXT NOT NULL,
    definition_version INTEGER NOT NULL,
    definition_version_hash TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    state_map_hash TEXT NOT NULL REFERENCES computation_state_maps (state_map_hash),
    outcome TEXT NOT NULL,
    value REAL,
    passes_counted INTEGER NOT NULL,
    issues_excluded INTEGER NOT NULL,
    computed_at TEXT NOT NULL,
    UNIQUE (
        team, period, definition_id, definition_version, definition_version_hash,
        snapshot_hash, state_map_hash
    ),
    -- Exception to the no-CHECK rule, F1 ADR 0009: outcome is a closed list, value is NULL only
    -- when no pass finished.
    CHECK (
        (outcome = 'value' AND value IS NOT NULL)
        OR (outcome = 'no_finished_passes' AND value IS NULL)
    )
) STRICT;

CREATE INDEX IF NOT EXISTS idx_computation_measurements_state_map
    ON computation_measurements (state_map_hash);
