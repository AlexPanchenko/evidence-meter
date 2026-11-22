"""The migration runner applies `NNNN_<name>.up.sql` in order and reverts with `.down.sql`."""

import sqlite3
from pathlib import Path

import pytest

from evidence_meter.platform.migrate import apply, revert_last


@pytest.fixture
def migrations(tmp_path: Path) -> Path:
    folder = tmp_path / "migrations"
    folder.mkdir()
    (folder / "0001_teams.up.sql").write_text("CREATE TABLE demo_team (name TEXT NOT NULL);")
    (folder / "0001_teams.down.sql").write_text("DROP TABLE demo_team;")
    (folder / "0002_periods.up.sql").write_text("CREATE TABLE demo_period (month TEXT NOT NULL);")
    (folder / "0002_periods.down.sql").write_text("DROP TABLE demo_period;")
    return folder


def tables(db: Path) -> set[str]:
    with sqlite3.connect(db) as conn:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    return {name for (name,) in rows} - {"schema_migrations"}


def test_apply_runs_pending_migrations_in_order(tmp_path: Path, migrations: Path) -> None:
    db = tmp_path / "demo.sqlite3"
    assert apply(db, migrations) == ["0001_teams", "0002_periods"]
    assert tables(db) == {"demo_team", "demo_period"}


def test_apply_twice_changes_nothing(tmp_path: Path, migrations: Path) -> None:
    db = tmp_path / "demo.sqlite3"
    apply(db, migrations)
    assert apply(db, migrations) == []


def test_revert_last_undoes_only_the_newest(tmp_path: Path, migrations: Path) -> None:
    db = tmp_path / "demo.sqlite3"
    apply(db, migrations)
    assert revert_last(db, migrations) == "0002_periods"
    assert tables(db) == {"demo_team"}
    assert apply(db, migrations) == ["0002_periods"]


def test_revert_on_an_empty_database_does_nothing(tmp_path: Path, migrations: Path) -> None:
    assert revert_last(tmp_path / "demo.sqlite3", migrations) is None


def test_a_failing_migration_leaves_no_partial_change(tmp_path: Path, migrations: Path) -> None:
    (migrations / "0003_broken.up.sql").write_text("CREATE TABLE demo_x (a TEXT); NOT SQL;")
    (migrations / "0003_broken.down.sql").write_text("DROP TABLE demo_x;")
    db = tmp_path / "demo.sqlite3"
    with pytest.raises(sqlite3.Error):
        apply(db, migrations)
    assert tables(db) == {"demo_team", "demo_period"}


def test_a_badly_named_migration_is_rejected(tmp_path: Path, migrations: Path) -> None:
    (migrations / "3_Oops'.up.sql").write_text("SELECT 1;")
    with pytest.raises(ValueError, match="NNNN_lower_snake"):
        apply(tmp_path / "demo.sqlite3", migrations)
