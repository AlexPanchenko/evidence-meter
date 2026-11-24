"""Static self-check of SQLite migration pairs (data-model-builder step 11.1).

Usage: python check_migrations.py <dir> [<dir> ...] [--prefixes collection,computation,...]

Checks every NNNN_<name>.up.sql under the given folders (recursively) and its .down.sql:
1. naming: NNNN_<verb>_<entity>, context-prefixed plural snake_case tables;
2. down reverses up: every CREATE TABLE / CREATE INDEX / ADD COLUMN has its DROP, children first;
3. FK index: each REFERENCES column leads some index in the same file;
4. forbidden: TRIGGER, VIEW, DEFAULT, CONCURRENTLY, BEGIN/COMMIT, Postgres types,
   CHECK without an ADR;
5. STRICT on every CREATE TABLE;
6. no foreign key to another context's table;
7. no column that could hold a person.
Exit 0 when all pass, 1 with file:line findings otherwise.
"""

import argparse
import re
import sys
from pathlib import Path

VERBS = "create|add|expand|backfill|contract|drop|seed|rename"
NAME = re.compile(rf"\d{{4}}_(init|({VERBS})_[a-z0-9_]+)")
CREATE_TABLE = re.compile(
    r"CREATE TABLE (?:IF NOT EXISTS )?(\w+)\s*\((.*?)\)\s*(STRICT)?\s*;", re.S
)
FORBIDDEN = re.compile(
    r"CREATE TRIGGER|CREATE VIEW|\bDEFAULT\b|CONCURRENTLY|^\s*(BEGIN|COMMIT)\b"
    r"|\b(VARCHAR|TIMESTAMPTZ|UUID|JSONB|SERIAL)\b",
    re.I,
)
PERSON = re.compile(
    r"^(assignee|author|reporter|creator|user|username|user_id|email|person|person_id|"
    r"owner|full_name|first_name|last_name|login|account_id)$"
)


def _strip_comments(sql: str) -> str:
    return re.sub(r"--[^\n]*", "", sql)


def check_pair(up: Path, prefixes: list[str]) -> list[str]:
    name = up.name.removesuffix(".up.sql")
    down = up.with_name(f"{name}.down.sql")
    raw = up.read_text()
    sql = _strip_comments(raw)
    found: list[str] = []
    if not NAME.fullmatch(name):
        found.append(f"{up}: name must be NNNN_<{VERBS}>_<entity>")
    if not down.exists():
        return [*found, f"{up}: no {down.name}"]
    down_sql = _strip_comments(down.read_text())
    rebuild = "RENAME TO" in sql

    tables = CREATE_TABLE.findall(sql)
    for table, body, strict in tables:
        prefix = table.split("_", 1)[0]
        context = next((p for p in prefixes if table.startswith(f"{p}_")), None)
        if context is None or not re.fullmatch(r"[a-z_]+s(_new)?", table):
            found.append(f"{up}: table {table}: plural snake_case with a context prefix {prefixes}")
        if not strict:
            found.append(f"{up}: table {table} is not STRICT")
        for ref in re.findall(r"REFERENCES (\w+)", body):
            if context and not ref.startswith(f"{context}_"):
                found.append(f"{up}: {table} references {ref} in another context ({prefix})")
        for line in body.splitlines():
            column = line.strip().split(" ", 1)[0].strip(",")
            if PERSON.match(column):
                found.append(f"{up}: {table}.{column} could hold a person")
        if (
            "IF NOT EXISTS" in sql
            and not table.endswith("_new")
            and not re.search(rf"DROP TABLE IF EXISTS {table}\b", down_sql)
        ):
            found.append(f"{down}: no DROP TABLE IF EXISTS {table}")
    created = [t for t, _, _ in tables if not t.endswith("_new")]
    dropped = re.findall(r"DROP TABLE IF EXISTS (\w+)", down_sql)
    order = [t for t in dropped if t in created]
    if not rebuild and order != created[::-1][: len(order)]:
        found.append(f"{down}: drop tables in reverse order of creation (children first)")
    for index in re.findall(r"CREATE INDEX IF NOT EXISTS (\w+)", sql):
        if not rebuild and f"DROP INDEX IF EXISTS {index}" not in down_sql:
            found.append(f"{down}: no DROP INDEX IF EXISTS {index}")
    for column in re.findall(r"ADD COLUMN (\w+)", sql):
        if f"DROP COLUMN {column}" not in down_sql:
            found.append(f"{down}: no DROP COLUMN {column}")
    for column in re.findall(r"(\w+) \w+ NOT NULL REFERENCES", sql):
        if not re.search(rf"ON \w+ \(\s*{column}\b", sql):
            found.append(f"{up}: foreign key {column} has no index that starts with it")
    for number, line in enumerate(_strip_comments(raw).splitlines(), 1):
        if FORBIDDEN.search(line):
            found.append(f"{up}:{number}: forbidden: {line.strip()}")
        if "CHECK" in line.upper() and not re.search(r"ADR \d{4}", raw):
            found.append(f"{up}:{number}: CHECK without an ADR number in a comment")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dirs", nargs="+", type=Path)
    parser.add_argument(
        "--prefixes", default="collection,computation,definitions,evidence_guard,reporting"
    )
    args = parser.parse_args(argv)
    prefixes = args.prefixes.split(",")
    ups = sorted(p for d in args.dirs for p in d.rglob("*.up.sql"))
    found = [f for up in ups for f in check_pair(up, prefixes)]
    for line in found:
        print(line)
    print(f"check_migrations: {len(ups)} up files, {len(found)} findings")
    return 1 if found or not ups else 0


if __name__ == "__main__":
    sys.exit(main())
