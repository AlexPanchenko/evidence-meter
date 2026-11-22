"""Regression tests for the path-scoped rules in .claude/rules/.

AE 3.0 m04-l05 and the module 4 checklist. A rule with `paths:` loads only when Claude reads a
matching file, so a wrong glob silently turns the rule off. Each context rule is pinned to its
context folder and must match a real file there.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / ".claude" / "rules"


def _paths(text: str) -> list[str]:
    head, sep, _ = text.removeprefix("---\n").partition("\n---\n")
    assert text.startswith("---\n") and sep, "rule must start with a --- frontmatter block"
    return [
        line.strip()[2:].strip('"') for line in head.splitlines() if line.strip().startswith("- ")
    ]


@pytest.mark.parametrize("context", ["computation", "evidence_guard"])
def test_context_rule_is_scoped_to_its_folder(context: str) -> None:
    rule = RULES / f"{context}.md"
    assert _paths(rule.read_text()) == [f"src/evidence_meter/{context}/**"]


@pytest.mark.parametrize("context", ["computation", "evidence_guard"])
def test_context_rule_glob_matches_a_real_file(context: str) -> None:
    (glob,) = _paths((RULES / f"{context}.md").read_text())
    folder = ROOT / glob.removesuffix("/**")
    assert any(p.is_file() for p in folder.rglob("*"))
