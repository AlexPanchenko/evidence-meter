---
status: Accepted
date: 2026-11-22
---

# ADR 0001: Stack — Python 3.12 with FastAPI, argparse and SQLite; React with Vite for the web app

## Context and problem statement

Evidence Meter collects tracker and Git data, computes metrics, refuses unsupported values and drafts a
monthly page. The v1 has a CLI, a backend API and a web app (kept in v1 on purpose, to learn each
surface). The stack is the costliest choice to change later.

## Decision drivers

- One main language for the logic, so metric code and tests read in one place.
- Few dependencies: each is a licence and an upgrade cost in a public repository.
- Each course artifact (OpenAPI contract, SQL migrations, UI line) has a standard tool.

## Considered options

1. Python 3.12 + FastAPI + argparse + SQLite + React/Vite/TypeScript.
2. Python CLI only, server-rendered page later (Jinja2), no separate web app.
3. Go backend + React (the SDLC `scaffold` template).

## Decision outcome

Option 1. Python keeps the metric logic in the language of the earlier prototype; FastAPI serves the
OpenAPI contract; argparse and `sqlite3` come with the standard library; React with Vite is the most
common web setup and fits the course's UI tooling.

### Consequences

- Good: logic, CLI and API share one package and one test runner (pytest).
- Bad: two toolchains (uv and npm), two lint and test setups; `make` wraps both.
- Bad: option 2 would have been smaller; the web app is kept for learning, not for a current need.
