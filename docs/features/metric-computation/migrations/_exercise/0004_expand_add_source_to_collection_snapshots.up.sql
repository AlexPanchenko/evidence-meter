-- Exercise (m06-l05 hard level), not promoted. Step 1 of 3, expand: add the column nullable.
-- From this release the app writes source on every new snapshot.
ALTER TABLE collection_snapshots ADD COLUMN source TEXT;
