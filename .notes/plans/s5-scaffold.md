# S5 plan: Evidence Meter scaffold (m04-l06, m04-l10, m04-checklist)

## Context

S3 fixed five bounded contexts in `docs/bc-map.md` (Collection, Definitions, Computation, Evidence Guard,
Reporting). S5 materialises them as a skeleton: `/sdlc:map-architecture` writes the foundation, then the
skeleton is built from its `tasks.json`, with no business code. The plan itself is the m04-l06 evidence
(one Plan-mode run with a 3-wave interview, no run without the interview, no Ctrl+G: partial coverage).

Repo `evidence-meter`, branch `main`, clean, HEAD `a3893f8`. Must not change:
`.claude/settings*.json`, existing CLAUDE.md rules (wording), `docs/bc-map.md` boundaries, existing tests.

## Interview answers (3 waves, 11 questions)

| # | Question | Answer |
|---|---|---|
| 1 | Layer depth | "Don't know"; later: default accepted, empty layer subpackages |
| 2 | Cross-context imports | Nothing; only `evidence_meter.shared` |
| 3 | Entry point | Owner: keep backend and frontend services in v1 for learning |
| 4 | Persistence | Stdlib migration runner now |
| 5 | Runnable parts | CLI + FastAPI backend + frontend app |
| 6 | Backend security | Owner asked about Google auth; accepted: ADR now (OIDC, provider from env, Google Workspace first), code with the first data-serving feature, localhost bind until then |
| 7 | CLAUDE.md | Append Architecture section, update Commands |
| 8 | l06 evidence | `.notes/plans/s5-scaffold.md` + tag |
| 9 | Frontend stack | Vite + React + TypeScript |

What the interview changed: a frontend app and backend service (I had proposed CLI only); a migration
runner now (I had proposed deferring to S7); an auth ADR (not in the first draft).
Trap caught before code: Google auth in the scaffold would have put a real organisation's domain and
OAuth client into a public repo and made `make dev` fail on a clean clone.

## Steps and commits

1. **[m04-l06]** Copy this plan to `.notes/plans/s5-scaffold.md`; commit; tag `ae3/m04-l06`.
2. **[m04-l10] `/sdlc:map-architecture`** with the homework prompt (idea in README, contexts and structure
   from `docs/bc-map.md`, no new contexts, stack and conventions in CLAUDE.md, do not overwrite CLAUDE.md).
   Answers: calibration "pick good defaults, I'll confirm"; intent "CLI + HTTP API + web app";
   foundation per this plan. Check: map lists exactly the 5 contexts + `reflects_commit`; ADRs for stack and
   style in `docs/adr/`; `docs/features/_scaffold/tasks/tasks.json`. Add ADR "Auth: OIDC, deferred".
   Commit subject `[m04-l10] map-architecture: greenfield foundation + scaffold plan` (fix prefix if the
   skill commits without it; local, unpushed).
3. **[m04-l10] Dependencies** (approval of this plan = the "ask first"): check on PyPI/npm that each exists,
   is maintained, licence fits a public repo, and report it. Python: `fastapi`, `uvicorn` (runtime),
   `httpx` (dev, TestClient). `web/`: `create-vite` pinned, `react-ts` template (react, react-dom, vite,
   typescript, eslint), plus `vitest` dev. All local; nothing global.
4. **[m04-l10] Skeleton**, test first where there is behaviour:
   - `tests/test_architecture.py` (stdlib `ast`): a context imports no other context and no entrypoint;
     `shared` and `platform` import no context; Computation `domain` imports no `app`/`infra`/third-party;
     handler→service→repo one direction. Checker proved on synthetic violating sources, then on `src/`.
   - `src/evidence_meter/<context>/` for `collection`, `definitions`, `evidence_guard`, `reporting`
     (`handler/`, `service/`, `repo/`) and `computation` (`domain/`, `app/`, `infra/`): `__init__.py`
     docstrings only, plus `README.md` per context (purpose, 3-5 glossary terms, events published and
     listened to, from bc-map).
   - `shared/` (kernel, empty), `platform/migrate.py` (stdlib `sqlite3`: applies `migrations/*.sql` in
     order, records them in `schema_migrations`, idempotent; DB path from `EVIDENCE_METER_DB`, default
     `var/evidence-meter.sqlite3`), tested on a temp DB with fixture migrations.
   - `entrypoints/cli.py` (argparse, `evidence-meter` script) and `entrypoints/api.py` (FastAPI, `/health`
     only); smoke tests: `main(["--help"])`, TestClient `/health` → 200.
   - `web/`: Vite React-TS app, one smoke test (Vitest), ESLint.
   - `Makefile`: `sync` (+ `npm --prefix web ci`), `dev` (uvicorn on 127.0.0.1:8000 + Vite, `make -j2`),
     `test` (pytest + vitest), `lint` (ruff + architecture test + eslint), `migrate`, `format`,
     `check` = lint + test.
   - `.env.example` names only (tracker URL, tracker token, Git repo path, definitions file path, DB path,
     OIDC issuer/client id/secret); `.gitignore`: `.env`, `var/`, `web/node_modules`, `web/dist`.
   - `ARCHITECTURE.md` ≤60 lines (style, dependency rule, where logic lives, link to the map; publishers and
     listeners of the main events); `SPEC.md` (goals, non-goals, key decisions, v1 acceptance criteria).
   - CLAUDE.md: Commands updated, new Architecture section (dependency rule, `@ARCHITECTURE.md`, where
     SPEC/map/ADRs live), under 200 lines.
   - Commit `[m04-l10] initial scaffold: Python 3.12 FastAPI + React/Vite, modular monolith`
     (split backend / web / docs if large). Deviations from `tasks.json` reported, map updated if needed.
5. Tag `ae3/m04-l10` after the owner's fresh-session check; `ae3/m04-checklist` after the owner's `/context`
   screenshot. Owner pushes with `! git push --follow-tags`.

## Verification

- `make check` → ruff, architecture test, pytest, eslint, vitest all green; show last lines.
- Architecture test red first (planted violation), green on `src/`.
- `make dev` starts both, stopped after start (if the sandbox blocks binding a port: owner runs `! make dev`).
- `tree -L 3 -I '.git|node_modules|.venv'`; `git status` shows no `.env`.
- Owner, fresh session: `/context` lists CLAUDE.md and ARCHITECTURE.md; homework step-5 prompt with
  `MetricComputed`; Claude must name the file for each answer.

## Open / not verified

- npm and PyPI reachability from the sandbox (will list hosts in `allowed_domains`).
- What `map-architecture` proposes beyond this plan (e.g. CI); anything conflicting is raised, not applied.
