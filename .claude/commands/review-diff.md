---
description: Review the current git diff against the rules in AGENTS.md
---
Review `git diff main...HEAD` and the uncommitted changes (`git diff HEAD`).

Check:
1. Every rule in AGENTS.md (imported by CLAUDE.md) and `.claude/rules/` that the change touches.
2. New behaviour has a test; a metric has golden data with expected values computed by hand.
3. Nothing outside the task changed.

Report each finding as: file, line, problem, fix. Say "no findings" when there are none.
