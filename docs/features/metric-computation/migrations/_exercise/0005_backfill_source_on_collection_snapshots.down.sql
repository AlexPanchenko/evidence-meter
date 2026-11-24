-- Back to the state after expand; rows written by the app after expand also lose source (see
-- backfill-source.md).
UPDATE collection_snapshots SET source = NULL;
