"""Platform helpers for F1 task T2: configuration from the environment, one transaction per command.

`config.load` reads `EVIDENCE_METER_DB` and `EVIDENCE_METER_DEFINITIONS` and never opens the
definitions file; `db.transaction` opens a connection with foreign keys on and commits all or
nothing.
(docs/features/metric-computation/tasks/T2-platform-config-db.md, sad.md §8, data-model.md flags)
"""

import sqlite3
from pathlib import Path

import pytest

from evidence_meter.platform.config import Config, load
from evidence_meter.platform.db import connect, transaction
from evidence_meter.platform.migrate import apply

MIGRATIONS = Path(__file__).resolve().parent.parent / "migrations"
SNAPSHOT = (
    "INSERT INTO collection_snapshots (team, period, snapshot_hash, imported_at) "
    "VALUES ('team-alpha', '2026-10', 'hash-demo-1', '2026-11-01T00:00:00Z')"
)


@pytest.fixture
def db(tmp_path: Path) -> Path:
    path = tmp_path / "evidence-meter.sqlite3"
    apply(path, MIGRATIONS)
    return path


def snapshot_count(path: Path) -> int:
    with sqlite3.connect(path) as conn:
        return conn.execute("SELECT count(*) FROM collection_snapshots").fetchone()[0]


def test_load_reads_both_variables(tmp_path: Path) -> None:
    env = {
        "EVIDENCE_METER_DB": str(tmp_path / "demo.sqlite3"),
        "EVIDENCE_METER_DEFINITIONS": str(tmp_path / "definitions-demo.toml"),
    }
    assert load(env, home=tmp_path / "home") == Config(
        db=tmp_path / "demo.sqlite3", definitions=tmp_path / "definitions-demo.toml"
    )


def test_load_defaults_definitions_under_home_without_reading_it(tmp_path: Path) -> None:
    home = tmp_path / "home"  # does not exist: loading must not open the file
    config = load({"EVIDENCE_METER_DB": str(tmp_path / "demo.sqlite3")}, home=home)
    assert config.definitions == home / ".config" / "evidence-meter" / "definitions.toml"
    assert not home.exists()


def test_connect_turns_foreign_keys_on(db: Path) -> None:
    conn = connect(db)
    try:
        assert conn.execute("PRAGMA foreign_keys").fetchone() == (1,)
    finally:
        conn.close()


def test_transition_for_a_missing_snapshot_is_rejected(db: Path) -> None:
    with pytest.raises(sqlite3.IntegrityError), transaction(db) as conn:
        conn.execute(
            "INSERT INTO collection_issue_transitions "
            "(snapshot_id, issue_key, from_state, to_state, transitioned_at) "
            "VALUES (999, 'PRJ-DEMO-1', 'todo', 'done', '2026-10-02T00:00:00Z')"
        )


def test_transaction_commits_on_success(db: Path) -> None:
    with transaction(db) as conn:
        conn.execute(SNAPSHOT)
    assert snapshot_count(db) == 1


def test_error_inside_the_transaction_leaves_the_database_unchanged(db: Path) -> None:
    with pytest.raises(RuntimeError, match="demo failure"), transaction(db) as conn:
        conn.execute(SNAPSHOT)
        raise RuntimeError("demo failure")
    assert snapshot_count(db) == 0
