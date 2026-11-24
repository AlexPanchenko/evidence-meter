# Git guards (draft, AE 3.0 m06-l08)

Two guards for the Git rules in [AGENTS.md](../../AGENTS.md#git). `.claude/hooks/` and `.claude/settings.json`
are write-denied for Claude, so the owner installs both.

## 1. Hook: block staging a secret

```sh
mkdir -p .claude/hooks && cp docs/hooks-draft/block_secret_staging.py .claude/hooks/
```

`tests/test_secret_hook.py` runs the installed copy when it exists, else this draft (21 cases: explicit
paths, `-f`, broad adds, `commit -a`, safe commands). Known limit: a broad add after `cd <dir>` in the same
command is checked against the project root, not `<dir>`.

## 2. Settings: deny `git reset --hard`, register the hook

Add to `.claude/settings.json`:

```json
"permissions": {
  "deny": [
    "Bash(git reset --hard)",
    "Bash(git reset --hard *)"
  ]
},
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        { "type": "command", "command": "python3 -I \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block_secret_staging.py" }
      ]
    }
  ]
}
```

The two deny entries join the existing `deny` list; `hooks` is a new top-level key. After the edit, Claude
adds the settings tests (`tests/test_permissions.py`, per `.claude/rules/tests.md`) and proves both guards
fire in a live session: a `git reset --hard` call is denied, and `git add` of a planted `.env.local` file is
blocked with exit 2.
