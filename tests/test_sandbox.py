"""Regression tests for the sandbox block in .claude/settings.json (AE 3.0 m03-l07).

Permission rules see only the command Claude runs, not the files a child process opens
(a build script, a Makefile target). The OS sandbox closes that gap.
"""

import pytest

# Package index only; a new host needs a deliberate settings change.
ALLOWED_DOMAINS = {"pypi.org", "files.pythonhosted.org"}


def _sandbox(settings: dict) -> dict:
    return settings["sandbox"]


def test_sandbox_is_enabled_for_the_team(settings: dict) -> None:
    # /sandbox writes only to settings.local.json; the team setting must be in the project file.
    assert _sandbox(settings)["enabled"] is True


def test_session_fails_when_sandbox_is_unavailable(settings: dict) -> None:
    assert _sandbox(settings)["failIfUnavailable"] is True


def test_no_command_leaves_the_sandbox(settings: dict) -> None:
    # Strict mode: no "run unsandboxed" escape, not even with a prompt.
    assert _sandbox(settings)["allowUnsandboxedCommands"] is False


def test_network_allowlist_is_exact(settings: dict) -> None:
    domains = set(_sandbox(settings)["network"]["allowedDomains"])
    assert domains == ALLOWED_DOMAINS
    assert not [d for d in domains if "*" in d]


def test_extra_writes_stay_inside_the_uv_cache(settings: dict) -> None:
    assert _sandbox(settings)["filesystem"]["allowWrite"] == ["~/.cache/uv"]


@pytest.mark.parametrize("home_dir", ["~/.ssh", "~/.aws"])
def test_credential_dirs_are_closed_to_child_processes(settings: dict, home_dir: str) -> None:
    # Explicit in the sandbox, so it does not depend on Read deny rules being carried over.
    assert home_dir in _sandbox(settings)["filesystem"]["denyRead"]
    # The Read deny rule stays too: it covers Claude's own Read tool and simple cat/head.
    assert f"Read({home_dir}/**)" in settings["permissions"]["deny"]
