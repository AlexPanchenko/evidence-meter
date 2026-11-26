"""Configuration from the environment: the SQLite file and the private definitions file.

`load` only builds paths; it never opens the definitions file, which stays outside git and is read
by the Definitions context alone. See sad.md §8 Configuration.
"""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from evidence_meter.platform.migrate import DEFAULT_DB

DB_VAR = "EVIDENCE_METER_DB"
DEFINITIONS_VAR = "EVIDENCE_METER_DEFINITIONS"
DEFINITIONS_UNDER_HOME = Path(".config") / "evidence-meter" / "definitions.toml"


@dataclass(frozen=True)
class Config:
    """Paths the tool needs at run time."""

    db: Path
    definitions: Path


def load(env: Mapping[str, str] | None = None, home: Path | None = None) -> Config:
    """Build a `Config` from `env` (default `os.environ`); definitions default under `home`."""
    env = os.environ if env is None else env
    home = Path.home() if home is None else home
    db = Path(env[DB_VAR]) if env.get(DB_VAR) else DEFAULT_DB
    definitions = (
        Path(env[DEFINITIONS_VAR]) if env.get(DEFINITIONS_VAR) else home / DEFINITIONS_UNDER_HOME
    )
    return Config(db=db, definitions=definitions)
