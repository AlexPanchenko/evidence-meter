# Evidence Meter

Turns a written guide of engineering metrics into a tested tool: collect from an issue tracker and Git,
compute each metric from a versioned definition, refuse a value the data cannot support, draft a monthly
page for a person to review. Python 3.12 with uv; the package lives in `src/evidence_meter/`, the web
app (React, Vite, TypeScript) in `web/`.

## Commands

- `make sync`: install or update both environments after a change to `pyproject.toml`, `uv.lock` or
  `web/package-lock.json`.
- `make check`: `make lint` plus `make test`. This is the command that proves a change; run it before
  calling any task done and show its last lines.
- `make lint`: ruff lint and format check, the dependency rule (`tests/test_architecture.py`), oxlint and
  the TypeScript type check.
- `make test`: pytest and Vitest.
- `make dev`: the API on 127.0.0.1:8000 and the web app on 127.0.0.1:5173; stop it after use.
- `make migrate`: apply pending SQL migrations to `$EVIDENCE_METER_DB`.
- `make diagrams`: render every Mermaid block with mermaid-cli; run it after changing a diagram. It needs
  Chromium, which cannot start in the agent sandbox, so ask the owner to run it there; CI runs it too.
- `make format`: apply ruff formatting. Run it instead of fixing format findings by hand.
- `uv run pytest tests/<file>.py -k <name>`: one test while iterating; finish with `make check`.

## Architecture

@ARCHITECTURE.md

- Dependency rule: a context imports only itself, `shared` and `platform`; never another context and never
  `entrypoints`. Inside a context imports point inward (`handler` → `service` → `repo`, `infra` → `app` →
  `domain`); Computation's `domain` imports only the standard library and `shared`.
- Contexts talk through events wired in `entrypoints/`; a change that needs one context to call another
  is a boundary question for `docs/bc-map.md` first, not an import.
- Where things are: [SPEC.md](SPEC.md) (v1 goals and acceptance criteria),
  [docs/architecture-map.md](docs/architecture-map.md) (full map), [docs/bc-map.md](docs/bc-map.md)
  (contexts, events, glossary), [docs/adr/](docs/adr/) (decisions), a `README.md` in each context folder,
  `docs/features/<slug>/` (feature documents), [.notes/plans/](.notes/plans/) (approved plans).

## Data: synthetic and public only

The repository and everything built from it may become public, and a public copy cannot be recalled.

- Test data, examples, fixtures, docs and commit messages use invented teams, projects, people and
  codes. If a value looks like it came from a real organisation (a client name, a project key, a person,
  an internal URL), stop and ask instead of committing it.
- An organisation's own metric codes, thresholds and identifiers live in a private definitions file
  outside git (`~/.config/evidence-meter/`, `*.private.*`, `identifiers.local.*`). Code reads them at run
  time; never copy their contents into the repository, a test or a message. Reading them is denied anyway.
- Results are team-level only. Do not add an output, a column or a log line that shows a value per person,
  because the tool must not become a ranking of people.

## Changes Claude does not make

- `.claude/settings.json` and `.claude/settings.local.json` are the team's controls and are write-denied
  for Claude. Propose a change in the chat; the owner edits the file, and `tests/test_permissions.py` and
  `tests/test_sandbox.py` pin the result.
- A new dependency (`uv add`) asks first. Before proposing one, check that it exists, is maintained and has
  a licence compatible with a public repository, and say which one you checked.
- `git push` is denied. The owner pushes with `git push --follow-tags`.

## How to work here

- Write the failing test before the code when the change has behaviour; a metric always gets golden data
  with expected values computed by hand, so a wrong formula cannot pass by matching itself.
- Prefer the standard library until a dependency removes real work; each dependency is a licence and
  upgrade cost in a repository meant to be read by others.
- Keep a change inside one part of the code where you can; when it has to cross parts, say so in the plan
  first, because those seams will become module boundaries.
- Tests under `tests/` follow [.claude/rules/tests.md](.claude/rules/tests.md) (loaded when you open a test).

## Git

The project is the capstone of the Agentic Engineering 3.0 course; the history is the evidence of the build.

- Branches: GitHub Flow. `main` stays green; each change goes on a short branch `<feature-or-step>-<topic>`
  (`f1-spec-package`, `f1-cli-compute`) that lives a day or two. The owner pushes it and opens a draft PR
  after the first commit, so review starts early; merge only through a reviewed PR.
- Commit subject: `[<lesson-id>] <type>(<scope>): <what>`, Conventional Commits after the lesson id, e.g.
  `[m06-l08] feat(cli): add compute command`; types `feat`, `fix`, `docs`, `test`, `refactor`, `chore`. A
  change for several lessons of one step names them all: `[m04-l02 m04-l04] docs: ...`. Earlier commits
  use `[<lesson-id>] <what>` and stay as they are.
- One or more commits per lesson, never one commit across unrelated lessons; one logical change per commit
  (split mixed changes before committing). Commit only what the lesson changed; `make check` passes first.
- Review the diff (`git diff --staged` or `/diff`) before every commit.
- Undo a committed change with `git revert`, never `git reset --hard` (denied). Never force-push.
- Never stage a secret: `.env`, `*.pem`, `*.key`, `credentials*` stay out of git (`.gitignore`); a
  PreToolUse hook blocks staging them.
- When a lesson's evidence is complete, tag the last commit `ae3/<lesson-id>` with `git tag -a`, because
  `git push --follow-tags` pushes only annotated tags. Never move a pushed tag.
