# Evidence Meter

Turns a written guide of engineering metrics into a tested tool: collect from an issue tracker and Git,
compute each metric from a versioned definition, refuse a value the data cannot support, draft a monthly
page for a person to review. Python 3.12 with uv; the package lives in `src/evidence_meter/`.

## Commands

- `make sync`: install or update the environment after a change to `pyproject.toml` or `uv.lock`.
- `make check`: ruff lint, ruff format check and pytest. This is the command that proves a change; run it
  before calling any task done and show its last lines.
- `make format`: apply ruff formatting. Run it instead of fixing format findings by hand.
- `uv run pytest tests/<file>.py -k <name>`: one test while iterating; finish with `make check`.

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

## Commits

The project is the capstone of the Agentic Engineering 3.0 course; the history is the evidence of the build.

- One or more commits per lesson, never one commit across unrelated lessons. Subject starts with the lesson
  id: `[m04-l04] <what changed>`; a change that serves several lessons of one step names them all:
  `[m04-l02 m04-l04] <what>`.
- When a lesson's evidence is complete, tag the last commit `ae3/<lesson-id>`. Never move a pushed tag and
  never force-push.
- Commit only what the lesson changed; `make check` passes before each commit.
