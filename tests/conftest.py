import json
from pathlib import Path

import pytest

SETTINGS = Path(__file__).resolve().parent.parent / ".claude" / "settings.json"


@pytest.fixture(scope="session")
def settings() -> dict:
    """The team's Claude Code settings, committed in the repository."""
    return json.loads(SETTINGS.read_text())
