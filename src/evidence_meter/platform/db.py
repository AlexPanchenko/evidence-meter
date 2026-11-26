"""SQLite access: connections with foreign keys on, and one transaction per command.

`transaction` commits everything on success and rolls everything back on any exception, so a
failing command leaves the database as it was. See sad.md §8 Transactions and data-model.md flags.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


def connect(db: Path) -> sqlite3.Connection:
    """Open `db` in autocommit mode with `PRAGMA foreign_keys = ON`; the caller closes it."""
    conn = sqlite3.connect(db, isolation_level=None)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def transaction(db: Path) -> Iterator[sqlite3.Connection]:
    """Yield a connection inside one transaction: commit on success, roll back on any error."""
    conn = connect(db)
    try:
        conn.execute("BEGIN")
        try:
            yield conn
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        conn.execute("COMMIT")
    finally:
        conn.close()
