"""Regression tests for the permission rules in .claude/settings.json (AE 3.0 m03-l04, m03-l06)."""

import pytest

SECRET_READ_DENIES = [
    "Read(.env)",
    "Read(.env.*)",
    "Read(*.pem)",
    "Read(*.key)",
    "Read(~/.ssh/**)",
    "Read(~/.aws/**)",
    "Read(**/credentials*)",
]
PRIVATE_DATA_DENIES = [
    "Read(*.private.*)",
    "Edit(*.private.*)",
    "Read(identifiers.local.*)",
    "Edit(identifiers.local.*)",
    "Read(~/.config/evidence-meter/**)",
    "Read(**/data/real/**)",
    "Read(**/data/raw/**)",
]


def _rules(settings: dict) -> dict[str, list[str]]:
    return settings["permissions"]


def test_schema_is_declared(settings: dict) -> None:
    assert settings["$schema"] == "https://json.schemastore.org/claude-code-settings.json"


@pytest.mark.parametrize("rule", SECRET_READ_DENIES + PRIVATE_DATA_DENIES)
def test_secrets_and_private_data_are_denied(settings: dict, rule: str) -> None:
    assert rule in _rules(settings)["deny"]


def test_no_write_rules(settings: dict) -> None:
    # Claude Code does not check Write(...) rules; Edit(...) covers writes.
    all_rules = [r for rules in _rules(settings).values() for r in rules]
    assert not [r for r in all_rules if r.startswith("Write(")]


@pytest.mark.parametrize("rule", ["Bash", "Bash(*)", "Bash(* --version)", "Bash(* --help)"])
def test_no_blanket_bash_allow(settings: dict, rule: str) -> None:
    assert rule not in _rules(settings)["allow"]


def test_commit_is_never_pre_allowed(settings: dict) -> None:
    assert not [r for r in _rules(settings)["allow"] if r.startswith("Bash(git commit")]


@pytest.mark.parametrize("rule", ["Bash(git reset --hard)", "Bash(git reset --hard *)"])
def test_hard_reset_is_denied(settings: dict, rule: str) -> None:
    # m06-l08: undo with git revert; reset --hard destroys uncommitted work.
    assert rule in _rules(settings)["deny"]


def test_secret_staging_hook_is_registered(settings: dict) -> None:
    # m06-l08: the PreToolUse hook blocks staging a secret (behaviour: tests/test_secret_hook.py).
    commands = [
        hook["command"]
        for entry in settings["hooks"]["PreToolUse"]
        if entry["matcher"] == "Bash"
        for hook in entry["hooks"]
    ]
    assert any(c.endswith("/.claude/hooks/block_secret_staging.py") for c in commands)
