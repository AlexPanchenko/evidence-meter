---
name: contract-builder
description: Derive a feature's interface contract (contracts/cli.md for a CLI, contracts/openapi.yaml for an HTTP route, contracts/events.md for in-process events) from data-model.md, sad.md §6 flows and the PRD's acceptance criteria, with a field-origins table, a 6-point drift check (the sixth is team-level privacy), refusal codes checked against the feature's closed list in its ADR, exit-code classes for commands, the repository's {"error": {code, message}} envelope for HTTP, and a reconcile mode that keeps a field whose column vanished as "# stale" instead of dropping it. Use when the owner says "contract for <slug>", "cli contract for <slug>", "api for <slug>" or "/contract-builder <slug>" in a modular-monolith repository whose results must stay team-level and public-safe. Needs docs/features/<slug>/PRD.md and sad.md with target_surfaces; writes docs/features/<slug>/contracts/, or another folder with --out-dir.
---

# contract-builder

A standalone variant of the SDLC plugin's `api-forge` skill, tuned to this repository: the first features
are command-line only (until OIDC, ADR 0004), refusals are typed results with a closed code list per
feature, the HTTP API wraps every error as `{"error": {"code", "message"}}` (`entrypoints/api.py`), contexts
talk through in-process events, and no output may show a value per person. Same flow as the plugin (gate,
surface, scenario, derive, errors from sequences, examples, drift check, report, reconcile); the changes are
listed at the end. It reads no file from the plugin.

## Inputs

- `<slug>`: kebab-case. Required: `docs/features/<slug>/PRD.md` (stop: "run prd-builder first") and
  `sad.md` with `target_surfaces` in its frontmatter (stop: "run sad-builder first"; never re-derive the
  surface).
- Read, in this order: `sad.md` frontmatter and §6 flows with their `alt`/`else` branches, §8 (capability
  rule, refusal codes, privacy ledger), `data-model.md` (scenario A if present, B if not), every feature ADR
  (the refusal ADR holds the closed code list), PRD §4-§5, `CONTEXT.md`, an existing contract (update in
  place, never overwrite).
- Optional: `--out-dir <dir>` (comparison run, touches nothing else), `--reconcile`, `--depth easy|medium`
  (easy: no Socratic pass, owner decisions only for flags; medium, the default: walk each command's table
  with the owner before writing).

## Hard rules

- **Never invent a field, flag, code or exit code.** Each one has an origin row in the report: a column, an
  AC, a §6 message, an owner decision recorded in the run, or a framework default (`--help`, top-level
  `--version`) named as such. A template field with no origin is deleted and
  listed under "Dropped for lack of an origin".
- **Never silently drop a field.** A field whose source vanished stays with `# stale` and a report row; the
  owner chooses: fix the contract or fix the source first.
- **Team-level only.** No flag, field, column, example or log line that names or counts a person. A breakdown
  by person is a documented refusal, not an option that is missing. `scripts/check_contract.py` fails on
  person words outside a refusal row.
- **Synthetic examples only:** `team-alpha`, `cycle-time`, `PRJ-DEMO-1`, states `Doing`, `Done`, hashes as
  `<sha256>`. No organisation, project key, tracker state or metric code from a real definitions file.
- Codes are the feature's closed list, in the ADR's form (bare snake_case), not `module.error_name`. A new
  code the flows need is a **proposal** row and a Deferral until the ADR lists it.
- Every commit passes `make check` and follows AGENTS.md "Commits".

## Protocol

### 1. Gate and surface
Check both inputs. Read `target_surfaces`: `cli` → `contracts/cli.md`; an HTTP route on `api.py` →
`contracts/openapi.yaml`; any published event → also `contracts/events.md`; none → write a one-line report
and stop. Say "scenario A" (data-model present) or "scenario B" in chat.

### 2. Rules (HTTP only)
If `.claude/rules/openapi.md` is missing, copy `templates/rules-openapi.md` and say so in chat. It fixes the
repository envelope, 127.0.0.1 binding until OIDC, cursor pagination and the ban list.

### 3. Copy the templates
`templates/cli.md`, `templates/openapi.yaml`, `templates/events.md` as the surface needs, and
`templates/report.md` → `contracts/contract-report.md`.

### 4. Derive commands or operations
Group user stories by the command or operation that serves them (several stories may share one command);
every story maps to at least one. A command that only serves a precondition (an import) maps to the AC
whose refusal names it. Every argument and output field gets an origin row. Constraints come across from
the model (`YYYY-MM`, `INTEGER ≥ 1`, CHECK enums).

### 5. Errors from the flows
Walk every `alt`/`else` branch of every §6 flow. Each one becomes an exit code and a reply (CLI) or a
response (HTTP). CLI exit codes are **classes**, not one per branch: 0 success (including idempotent
no-ops), 1 unexpected error, 2 usage error, 3 refusal (code on stderr), 4 defect. HTTP maps refusal →
409 or 422, usage → 400, defect → 500, all in the repository envelope.

### 6. Checks in order
For a command with several refusals, write the order table from SAD §6 (cheapest, no I/O first; all before
the first write). The order is part of the contract: a test can check that `--by person` refuses before the
definitions file is read.

### 7. Examples
Text output, refusal output and defect output for each command, synthetic values only.

### 8. Drift check and report
`contracts/contract-report.md`, Verdict line first (rules as the plugin: PASS, PASS (with deferrals),
FAIL), then field origins, the 6 points, unresolved origins, owner decisions, Deferrals:

1. *(core)* command/operation ↔ data-model: each reads or writes ≥1 table.
2. *(core)* refusal code ↔ the feature's closed list in its ADR (parsed from the ADR file, not remembered).
3. *(core)* argument constraint ↔ column type, format and CHECK.
4. *(supporting)* coverage: every table surfaced or marked internal; every AC has a reply; every command has a story.
5. *(supporting)* every §6 branch has an exit code or response; a reply with no branch is a sequence gap.
6. *(core)* privacy: no output field, flag, example or log line can name a person or carry a private name
   outside the local terminal (SAD §8 privacy ledger); `scripts/check_contract.py` must exit 0.

A **flag** is any point where the sources disagree, are silent on something the contract must fix (a
number, a name, a branch), or a default is overridden without an ADR. Three or more flags in one run: stop, ask the owner with AskUserQuestion (Accept as is / Fix the contract /
Save as OQ / Fix the source first), record each answer in "Owner decisions". Write the report on every run,
FAIL included.

### 9. Reconcile
`--reconcile` re-reads all inputs, tightens origins, marks fields whose source vanished `# stale`, writes a
"Reconcile run N" section on top and keeps the earlier runs below as history. The verdict is re-derived; each
earlier Deferral is closed or carried forward by name.

### 10. Codegen and proof
- CLI: no generator. The contract's proof is a test per row of the checks-in-order table and per exit-code
  class, written at build time (S9); list them in the report as "tests the contract implies".
- HTTP: `npx --yes openapi-typescript@7.13.0 contracts/openapi.yaml -o web/src/api/types.ts`, then
  `make lint` (its `tsc --noEmit` breaks on a removed or renamed field). The server is code-first
  (FastAPI): compare `app.openapi()` with the contract in a test instead of generating server stubs.

### 11. Self-check, commit, handoff
Run `python3 -I scripts/check_contract.py docs/features/<slug>/contracts` → exit 0. Propose one commit per
run (`[<lesson>] <slug> contract via contract-builder`). Hand off: PASS or PASS (with deferrals) →
`/sdlc:break-tasks <slug>`; FAIL → the source to fix, then `--reconcile`.

## What changed against the plugin's api-forge

- Surface-first: CLI and in-process events are the main path here; HTTP is the later case.
- Bare refusal codes from the feature's ADR replace `module.error_name`; checked against the ADR file.
- Exit-code classes (0-4) replace "one exit code per branch".
- The repository's `{"error": {code, message}}` envelope replaces `{code, message, details?}`.
- A sixth, core drift point: privacy (team-level only, no private names), enforced by a script.
- A "checks in order" table, because all-or-nothing depends on refusal order.
- Codegen is honest about the stack: no generator for a Python CLI; openapi-typescript for the web client;
  a contract test for the code-first FastAPI server.
- Removed: Idempotency-Key and retry/DLQ sections (no async transport), BearerAuth default (no sign-in until
  OIDC, ADR 0004), `/api/v1` versioning default (no data-serving route yet).
