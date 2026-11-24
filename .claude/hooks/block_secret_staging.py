"""PreToolUse hook: block a Bash command that would stage or commit a secret file (m06-l08).

Draft: the owner installs it as .claude/hooks/block_secret_staging.py (Claude cannot write there)
and registers it in .claude/settings.json; see docs/hooks-draft/README.md.

Reads the hook JSON on stdin. Exit 2 with a reason on stderr blocks the call; exit 0 lets it
through. Catches `git add <secret>`, `git add -f`, broad adds (`-A`, `--all`, `.`, `-u`) and
`git commit -a` or `git commit <paths>` when a secret file would be included. Stdlib only.
"""

import fnmatch
import json
import re
import shlex
import subprocess
import sys
from pathlib import PurePosixPath

SECRET_PATTERNS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "credentials*",
    "*.private.*",
    "identifiers.local.*",
)
ALLOWED = (".env.example",)
SEGMENT_SPLIT = re.compile(r"&&|\|\||;|\||\n")


def is_secret(path: str) -> bool:
    name = PurePosixPath(path.strip('"').rstrip("/")).name
    if name in ALLOWED:
        return False
    return any(fnmatch.fnmatch(name, pattern) for pattern in SECRET_PATTERNS)


def git_args(tokens: list[str]) -> tuple[list[str], list[str]] | None:
    """Return (global options, the rest) when the segment is a git command, else None."""
    if not tokens or PurePosixPath(tokens[0]).name != "git":
        return None
    i, options = 1, []
    while i < len(tokens) and tokens[i].startswith("-"):
        takes_value = tokens[i] in ("-C", "-c")
        options += tokens[i : i + 1 + takes_value]
        i += 1 + takes_value
    return options, tokens[i:]


def candidates(options: list[str], *, untracked: bool, ignored: bool) -> list[str]:
    """Paths a broad add or `commit -a` would pick up, from `git status`."""
    command = ["git", *options, "status", "--porcelain", "--untracked-files=all"]
    if ignored:
        command.append("--ignored")
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    paths = []
    for line in result.stdout.splitlines():
        status, path = line[:2], line[3:]
        if status == "??" and not untracked:
            continue
        if status == "!!" and not ignored:
            continue
        paths.append(path.split(" -> ")[-1])
    return paths


def secrets_in_segment(segment: str) -> list[str]:
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return []
    parsed = git_args(tokens)
    if parsed is None or not parsed[1]:
        return []
    options, (sub, *rest) = parsed
    flags = [t for t in rest if t.startswith("-")]
    paths = [t for t in rest if not t.startswith("-")]
    if sub in ("add", "stage"):
        force = any(f in ("-f", "--force") for f in flags)
        broad = any(f in ("-A", "--all", "-u", "--update") for f in flags) or "." in paths
        found = [p for p in paths if p != "." and is_secret(p)]
        if broad:
            untracked = not any(f in ("-u", "--update") for f in flags)
            found += [
                p for p in candidates(options, untracked=untracked, ignored=force) if is_secret(p)
            ]
        return found
    if sub == "commit":
        commit_all = any(
            f in ("-a", "--all") or re.fullmatch(r"-[a-zA-Z]*a[a-zA-Z]*", f) for f in flags
        )
        message_values = {rest[i + 1] for i, t in enumerate(rest[:-1]) if t in ("-m", "--message")}
        found = [p for p in paths if p not in message_values and is_secret(p)]
        if commit_all:
            found += [
                p for p in candidates(options, untracked=False, ignored=False) if is_secret(p)
            ]
        return found
    return []


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if event.get("tool_name") != "Bash":
        return 0
    command = event.get("tool_input", {}).get("command", "")
    found = sorted(
        {p for segment in SEGMENT_SPLIT.split(command) for p in secrets_in_segment(segment)}
    )
    if not found:
        return 0
    print(
        f"Blocked: this would stage a secret file ({', '.join(found)}). "
        "Keep secrets out of git (AGENTS.md, Git); add the file to .gitignore instead.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
