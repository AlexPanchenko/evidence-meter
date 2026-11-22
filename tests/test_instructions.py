"""Instruction files load as one chain: CLAUDE.md -> AGENTS.md -> ARCHITECTURE.md (AE 3.0 m04-l10).

Claude Code reads only CLAUDE.md when it exists, so CLAUDE.md must import AGENTS.md on its first
line; other agents read AGENTS.md directly. The size limits keep each session's context small.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def lines(name: str) -> list[str]:
    return (ROOT / name).read_text().splitlines()


def test_claude_md_imports_agents_md_first() -> None:
    assert lines("CLAUDE.md")[0] == "@AGENTS.md"


def test_agents_md_has_architecture_section_importing_architecture_md() -> None:
    agents = lines("AGENTS.md")
    assert "## Architecture" in agents
    assert "@ARCHITECTURE.md" in agents


@pytest.mark.parametrize(("name", "limit"), [("AGENTS.md", 200), ("ARCHITECTURE.md", 60)])
def test_instruction_file_stays_short(name: str, limit: int) -> None:
    assert len(lines(name)) <= limit


def test_rules_live_in_one_file_only() -> None:
    """No rule text is duplicated: CLAUDE.md holds only the import and Claude Code-only rules."""
    shared_sections = {line for line in lines("AGENTS.md") if line.startswith("## ")}
    claude_sections = {line for line in lines("CLAUDE.md") if line.startswith("## ")}
    assert shared_sections.isdisjoint(claude_sections)
