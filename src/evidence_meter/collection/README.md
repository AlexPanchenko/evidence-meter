# Collection

Reads the issue tracker and Git for one team and one period and keeps an immutable snapshot. It knows
trackers, fields and commits; it knows nothing about metrics.

- **Terms:** Source (tracker or Git), Snapshot, Issue, IssueState, Commit.
- **Publishes:** `TrackerSnapshotCollected`, `GitHistoryCollected`, `CollectionFailed`.
- **Listens to:** `ReportingPeriodClosed` (external trigger: the CLI or a scheduler).
- **Structure:** handler/service/repo; source adapters live in `repo/`.
