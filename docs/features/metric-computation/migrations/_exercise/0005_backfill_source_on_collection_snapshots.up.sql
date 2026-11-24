-- Exercise, step 2 of 3, backfill: every snapshot before this change came from a file import.
-- See backfill-source.md.
UPDATE collection_snapshots SET source = 'file' WHERE source IS NULL;
