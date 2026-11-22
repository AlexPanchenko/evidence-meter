"""Plain SQL migrations for SQLite: `NNNN_<name>.up.sql` in order, `.down.sql` to revert.

Each migration runs in its own transaction together with its row in `schema_migrations`, so a
failing file leaves the database as it was. See docs/adr/0003-persistence-sqlite.md.
"""

import argparse
import os
import re
import sqlite3
from pathlib import Path

DEFAULT_DB = Path("var/evidence-meter.sqlite3")
DEFAULT_MIGRATIONS = Path("migrations")
NAME = re.compile(r"\d{4}_[a-z0-9_]+")
TABLE = (
    "CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY, applied_at TEXT NOT NULL)"
)


def _connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db, isolation_level=None)
    conn.execute(TABLE)
    return conn


def _applied(conn: sqlite3.Connection) -> list[str]:
    return [name for (name,) in conn.execute("SELECT name FROM schema_migrations ORDER BY name")]


def _run(conn: sqlite3.Connection, script: str, record: str) -> None:
    # executescript commits any open transaction first, so BEGIN and COMMIT go inside the script.
    try:
        conn.executescript(f"BEGIN;\n{script}\n;\n{record};\nCOMMIT;")
    except sqlite3.Error:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise


def _names(migrations: Path) -> list[str]:
    names = sorted(p.name.removesuffix(".up.sql") for p in migrations.glob("*.up.sql"))
    bad = [name for name in names if not NAME.fullmatch(name)]
    if bad:
        raise ValueError(f"migration names must match NNNN_lower_snake: {bad}")
    return names


def apply(db: Path, migrations: Path) -> list[str]:
    """Apply every pending migration in name order; return the names applied."""
    conn = _connect(db)
    try:
        done = set(_applied(conn))
        pending = [name for name in _names(migrations) if name not in done]
        for name in pending:
            script = (migrations / f"{name}.up.sql").read_text()
            record = f"INSERT INTO schema_migrations VALUES ('{name}', datetime('now'))"
            _run(conn, script, record)
        return pending
    finally:
        conn.close()


def revert_last(db: Path, migrations: Path) -> str | None:
    """Revert the newest applied migration with its down file; return its name, or None if none."""
    conn = _connect(db)
    try:
        applied = _applied(conn)
        if not applied:
            return None
        name = applied[-1]
        script = (migrations / f"{name}.down.sql").read_text()
        _run(conn, script, f"DELETE FROM schema_migrations WHERE name = '{name}'")
        return name
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="evidence-meter-migrate", description=__doc__.splitlines()[0]
    )
    parser.add_argument("--revert", action="store_true", help="revert the newest migration")
    args = parser.parse_args(argv)
    db = Path(os.environ.get("EVIDENCE_METER_DB", DEFAULT_DB))
    if args.revert:
        print(f"reverted: {revert_last(db, DEFAULT_MIGRATIONS) or 'nothing'}")
    else:
        applied = apply(db, DEFAULT_MIGRATIONS)
        print(f"applied: {', '.join(applied) or 'nothing pending'} ({db})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
