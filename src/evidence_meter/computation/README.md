# Computation

Applies one definition version to one snapshot and produces a raw value with the inputs it used. The
formulas are pure functions in `domain/`, tested with hand-computed golden data and no I/O.

- **Terms:** Measurement (raw value plus inputs), Period, Team.
- **Publishes:** `MetricComputed`.
- **Listens to:** `TrackerSnapshotCollected`, `GitHistoryCollected`, `DefinitionVersionPublished`.
- **Structure:** domain/app/infra; `domain` imports only the standard library and `shared`.
