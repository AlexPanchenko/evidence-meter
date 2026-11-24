-- flow 3: find snapshot by team, period and hash
SELECT id FROM collection_snapshots WHERE team_id = ? AND period = ? AND snapshot_hash = ?
-- flow 1: latest snapshot for team and period
SELECT id, snapshot_hash FROM collection_snapshots WHERE team_id = ? AND period = ? ORDER BY imported_at DESC, id DESC LIMIT 1
-- flow 1: read collection_* (transitions of one snapshot)
SELECT issue_key, from_state, to_state, transitioned_at FROM collection_issue_transitions WHERE snapshot_id = ? ORDER BY issue_key, transitioned_at
-- flow 1: find measurement by key
SELECT outcome, value, passes_counted, issues_excluded FROM computation_measurements WHERE team_id = ? AND period = ? AND definition_id = ? AND version_number = ? AND version_hash = ? AND snapshot_hash = ? AND state_map_hash = ?
-- flow 1: insert its state map if new (look up by hash)
SELECT id FROM computation_state_maps WHERE state_map_hash = ?
