# Decisions

Main decisions for Evidence Meter so far, with the reason and what was rejected. Append new entries at the
end; do not rewrite old ones. Where the reason or the alternatives were not discussed, the entry says so.

## 2026-11-20 Stack: Python 3.12 with uv, pytest and ruff

- Decision: Python 3.12, uv for the environment, pytest, ruff; SQLite with plain SQL migrations; FastAPI
  for the read API, the MCP Python SDK, Jinja2 for the page. To be confirmed in ADR 0001.
- Why: the previous collector (v1) is Python, so results compare directly; each course artifact has a
  standard tool in this stack.
- Rejected: alternatives were not recorded.

## 2026-11-20 Synthetic and public data only; organisation definitions stay private

- Decision: the repository, the plugin, submissions and demos hold synthetic and public data only. An
  organisation's metric codes, thresholds and identifiers live in a private definitions file outside git.
- Why: the repository is opened to the curators for review, and a copy made while it is public cannot be
  recalled.
- Rejected: alternatives were not recorded.

## 2026-11-20 Team-level results only

- Decision: every output (CLI, API, MCP, page) reports a value per team and month, never per person.
- Why: reason not recorded (stated as a rule in the README and the proposal).
- Rejected: alternatives were not recorded.

## 2026-11-20 No fork of the SDLC plugin for now

- Decision: use the course's SDLC plugin as it is; build the skeleton by hand where its scaffold has no
  Python template; record each friction for a later decision.
- Why: the Python gap is in a separate template repository, the other differences are project files the
  skills tell us to edit, and upstream releases often.
- Rejected: forking now; it would need upkeep against frequent upstream releases. Decide on a fork or an
  upstream contribution after the capstone.

## 2026-11-22 Permission and sandbox controls are pinned by tests

- Decision: `.claude/settings.json` is covered by `tests/test_permissions.py` and `tests/test_sandbox.py`;
  the sandbox is strict (no unsandboxed commands, explicit read denies for `~/.ssh` and `~/.aws`).
- Why: a weakened settings copy failed 5 tests, so a silent edit to the controls is caught by `make check`.
- Rejected: alternatives were not recorded.
