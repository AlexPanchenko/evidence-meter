"""Round trip of staged migrations with the repository's own runner (data-model-builder step 11.2).

Usage: uv run python roundtrip.py --staged <dir> [--staged <dir>] [--live migrations]
       [--queries queries.sql] [--runner evidence_meter.platform.migrate]

Copies the live tree and the staged files to a temp folder, then with the runner's apply and
revert_last: apply all, apply again (must be a no-op), revert every staged file (structure must
equal the live tree alone), apply again (structure must equal the first apply). Structure is
compared through pragmas (columns, indexes, foreign keys, STRICT), not SQL text, because SQLite
rewrites a renamed table's SQL. With --queries (one statement per line, `?` for parameters), each
query's EXPLAIN QUERY PLAN must not contain a full SCAN. Exit 0 on success, 1 otherwise.
"""

import argparse
import importlib
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

Shape = dict[str, tuple[object, ...]]


def shape(db: Path) -> Shape:
    conn = sqlite3.connect(db)
    try:
        names = [
            name
            for (name,) in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' "
                "AND name NOT LIKE 'sqlite_%' AND name != 'schema_migrations' ORDER BY name"
            )
        ]
        out: Shape = {}
        for name in names:
            indexes = sorted(
                (
                    row[1],
                    row[2],
                    tuple(c[2] for c in conn.execute(f"PRAGMA index_info('{row[1]}')")),
                )
                for row in conn.execute(f"PRAGMA index_list('{name}')")
            )
            out[name] = (
                conn.execute(f"PRAGMA table_info('{name}')").fetchall(),
                indexes,
                conn.execute(f"PRAGMA foreign_key_list('{name}')").fetchall(),
                conn.execute(
                    "SELECT strict FROM pragma_table_list WHERE name = ?", (name,)
                ).fetchone(),
            )
        return out
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--staged", type=Path, action="append", required=True)
    parser.add_argument("--live", type=Path, default=Path("migrations"))
    parser.add_argument("--queries", type=Path)
    parser.add_argument("--runner", default="evidence_meter.platform.migrate")
    args = parser.parse_args(argv)
    runner = importlib.import_module(args.runner)

    work = Path(tempfile.mkdtemp(prefix="roundtrip-"))
    folder = work / "migrations"
    folder.mkdir()
    for source in [args.live, *args.staged]:
        for sql in source.glob("*.sql"):
            shutil.copy(sql, folder)
    staged = sorted(
        {p.name.removesuffix(".up.sql") for d in args.staged for p in d.glob("*.up.sql")}
    )
    failures: list[str] = []

    live_db = work / "live.sqlite3"
    live_only = work / "live-only"
    live_only.mkdir()
    for sql in args.live.glob("*.sql"):
        shutil.copy(sql, live_only)
    runner.apply(live_db, live_only)
    base = shape(live_db)

    db = work / "roundtrip.sqlite3"
    applied = runner.apply(db, folder)
    print(f"apply: {', '.join(applied)}")
    full = shape(db)
    again = runner.apply(db, folder)
    print(f"apply again: {again or 'nothing pending'}")
    if again:
        failures.append("second apply was not a no-op")
    reverted = [runner.revert_last(db, folder) for _ in staged]
    print(f"revert x{len(staged)}: {', '.join(str(r) for r in reverted)}")
    if reverted != staged[::-1]:
        failures.append(f"reverted {reverted}, expected {staged[::-1]}")
    if shape(db) != base:
        failures.append("structure after revert differs from the live tree alone")
    print(f"structure after revert == live tree alone: {shape(db) == base}")
    runner.apply(db, folder)
    print(f"structure after re-apply == first apply: {shape(db) == full}")
    if shape(db) != full:
        failures.append("structure after re-apply differs from the first apply")

    if args.queries:
        conn = sqlite3.connect(db)
        for query in filter(None, (q.strip() for q in args.queries.read_text().splitlines())):
            if query.startswith("--"):
                continue
            plan = [
                row[3]
                for row in conn.execute(f"EXPLAIN QUERY PLAN {query}", [1] * query.count("?"))
            ]
            scan = any(step.startswith("SCAN") for step in plan)
            print(f"{'FAIL' if scan else 'ok  '} {query[:70]} -> {'; '.join(plan)}")
            if scan:
                failures.append(f"full scan: {query}")
        conn.close()

    for failure in failures:
        print(f"FAIL: {failure}")
    print(f"roundtrip: {'pass' if not failures else 'fail'} ({len(staged)} staged files)")
    shutil.rmtree(work)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
