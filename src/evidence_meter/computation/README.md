# Computation

Applies one definition version to one snapshot and produces a raw value with the inputs it used. The
formulas are pure functions in `domain/`, tested with hand-computed golden data and no I/O.

- **Terms:** Measurement (raw value plus inputs), Input, FormulaId, Period, Team.
- **Publishes:** `MetricComputed`.
- **Listens to:** `TrackerSnapshotCollected`, `GitHistoryCollected`, `DefinitionVersionPublished`,
  `DefinitionVersionRetired` (stop computing new values with that version).
- **Structure:** domain/app/infra; `domain` imports only the standard library and `shared`.
