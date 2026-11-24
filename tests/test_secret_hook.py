"""The PreToolUse hook that blocks staging a secret file (AE 3.0 m06-l08).

Runs the installed hook (.claude/hooks/) when present, else the draft (docs/hooks-draft/), as
Claude Code does: hook JSON on stdin, exit 2 blocks. Each case runs in a throwaway git repository
under tmp_path.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
NAME = "block_secret_staging.py"
HOOK = next(
    p
    for p in (ROOT / ".claude" / "hooks" / NAME, ROOT / "docs" / "hooks-draft" / NAME)
    if p.exists()
)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text(".env\n")
    (tmp_path / "app.py").write_text("print('team-alpha')\n")
    return tmp_path


def run_hook(repo: Path, command: str, tool: str = "Bash") -> subprocess.CompletedProcess[str]:
    event = {"tool_name": tool, "tool_input": {"command": command}}
    return subprocess.run(
        [sys.executable, "-I", str(HOOK)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        cwd=repo,
        check=False,
    )


@pytest.mark.parametrize(
    "command",
    [
        "git add .env",
        "git add -f .env",
        "git add config/.env.local",
        "git add deploy/server.pem",
        "git add credentials.json",
        "git stage tls.key",
        "make check && git add .env",
        "git -C . add .env",
        'git commit -m "wip" .env.production',
    ],
)
def test_explicit_secret_paths_are_blocked(repo: Path, command: str) -> None:
    result = run_hook(repo, command)
    assert result.returncode == 2
    assert "secret" in result.stderr


@pytest.mark.parametrize(
    "command",
    [
        "git add app.py",
        "git add .env.example",
        "git add -A",
        "git commit -m 'mention .env in the message only'",
        "echo git add .env",
        "git status",
    ],
)
def test_safe_commands_pass(repo: Path, command: str) -> None:
    assert run_hook(repo, command).returncode == 0


def test_broad_add_with_an_unignored_secret_is_blocked(repo: Path) -> None:
    (repo / "prod.pem").write_text("not a real key\n")
    result = run_hook(repo, "git add -A")
    assert result.returncode == 2
    assert "prod.pem" in result.stderr


def test_ignored_secret_is_safe_for_a_plain_broad_add(repo: Path) -> None:
    (repo / ".env").write_text("TOKEN=placeholder\n")
    assert run_hook(repo, "git add .").returncode == 0


def test_forced_broad_add_picks_up_an_ignored_secret(repo: Path) -> None:
    (repo / ".env").write_text("TOKEN=placeholder\n")
    assert run_hook(repo, "git add -f .").returncode == 2


def test_commit_all_with_a_tracked_secret_change_is_blocked(repo: Path) -> None:
    (repo / "credentials.txt").write_text("placeholder\n")
    subprocess.run(["git", "add", "-f", "credentials.txt"], cwd=repo, check=True)
    (repo / "credentials.txt").write_text("changed placeholder\n")
    assert run_hook(repo, "git commit -am 'update'").returncode == 2


def test_other_tools_are_ignored(repo: Path) -> None:
    assert run_hook(repo, "git add .env", tool="Edit").returncode == 0


def test_bad_input_does_not_block(repo: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-I", str(HOOK)],
        input="not json",
        capture_output=True,
        text=True,
        cwd=repo,
    )
    assert result.returncode == 0
