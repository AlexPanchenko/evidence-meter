-- Computation: state maps used (by hash) and measurements keyed by every input (F1 ADR 0008, 0009).
CREATE TABLE IF NOT EXISTS computation_state_maps (
    id INTEGER PRIMARY KEY,
    state_map_hash TEXT NOT NULL UNIQUE,
    state_map_json TEXT NOT NULL,
    recorded_at TEXT NOT NULL
) STRICT;

-- Natural key: team, period, definition id, version number, version hash, snapshot hash,
-- state-map hash (SAD §8 ID strategy). snapshot_hash points at Collection by hash, no foreign key.
CREATE TABLE IF NOT EXISTS computation_measurements (
    id INTEGER PRIMARY KEY,
    team_id TEXT NOT NULL,
    period TEXT NOT NULL,
    definition_id TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    version_hash TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    state_map_hash TEXT NOT NULL REFERENCES computation_state_maps (state_map_hash),
    outcome TEXT NOT NULL,
    value REAL,
    passes_counted INTEGER NOT NULL,
    issues_excluded INTEGER NOT NULL,
    computed_at TEXT NOT NULL,
    UNIQUE (
        team_id, period, definition_id, version_number, version_hash, snapshot_hash, state_map_hash
    ),
    -- ADR 0009: outcome is a closed list; value is NULL only with no_finished_passes.
    CHECK (
        (outcome = 'value' AND value IS NOT NULL)
        OR (outcome = 'no_finished_passes' AND value IS NULL)
    )
) STRICT;

-- Foreign-key rule only: no flow queries measurements by state map.
CREATE INDEX IF NOT EXISTS idx_computation_measurements_state_map
    ON computation_measurements (state_map_hash);
