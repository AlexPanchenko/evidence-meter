"""Regression tests for the project slash commands in .claude/commands/ (AE 3.0 m04-l03).

A command is shared through git like CLAUDE.md, so its contract is pinned here: it has a description
for the command menu and it reviews against the project's own rules.
"""

from pathlib import Path

import pytest

COMMANDS = Path(__file__).resolve().parent.parent / ".claude" / "commands"


def _frontmatter(text: str) -> dict[str, str]:
    head, sep, _ = text.removeprefix("---\n").partition("\n---\n")
    assert text.startswith("---\n") and sep, "command must start with a --- frontmatter block"
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


@pytest.fixture(scope="module")
def review_diff() -> str:
    return (COMMANDS / "review-diff.md").read_text()


def test_review_diff_has_a_description(review_diff: str) -> None:
    assert _frontmatter(review_diff)["description"].strip()


@pytest.mark.parametrize("source", ["CLAUDE.md", ".claude/rules/"])
def test_review_diff_checks_against_project_rules(review_diff: str, source: str) -> None:
    assert source in review_diff


def test_review_diff_reports_file_line_problem_fix(review_diff: str) -> None:
    assert "file, line, problem, fix" in review_diff
