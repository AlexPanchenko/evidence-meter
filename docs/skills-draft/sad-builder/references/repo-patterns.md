# Repo patterns for sad-builder

What a SAD in this repository starts from. Sources: `AGENTS.md`, `ARCHITECTURE.md`, `docs/bc-map.md`,
`docs/architecture-map.md`, repo `docs/adr/`. If one of them disagrees with this file, they win and this
file is stale; say so in the handoff.

**Reference SAD:** `docs/features/metric-computation/sad.md` with its `adr/` (the first feature). Use it
for tone, depth and section shape, not as content to copy.

## Recommended containers (§5)

Start §5 from this list; drop what the feature does not touch. A new kind of container is a decision.

| Container | C4 element | Technology | Note |
|---|---|---|---|
| CLI (entrypoints) | `Container(cli, ...)` | Python, argparse | Surface `cli`; orchestrates a run; the only wiring place with the API |
| Backend API (entrypoints) | `Container(api, ...)` | Python, FastAPI | Surface `backend-service`; 127.0.0.1 only until OIDC (repo ADR 0004) |
| Web app | `Container(web, ...)` | React, Vite, TypeScript | Surface `web-frontend`; calls `/api`; reuses map §Frontend |
| Collection | `Container(collection, ...)` | Python package | Snapshots of tracker and Git data; adapters in `repo/` |
| Definitions | `Container(definitions, ...)` | Python package | Versions, retirements, state maps from the private file |
| Computation | `Container(computation, ...)` | Python package | Pure formulas in `domain/`; measurements |
| Evidence Guard | `Container(guard, ...)` | Python package | Verdicts: accepted or refused with a reason |
| Reporting | `Container(reporting, ...)` | Python package | Monthly page: draft, review, publication |
| Local database | `ContainerDb(db, ...)` | SQLite | Tables prefixed by owning context; `schema_migrations` |
| Private definitions file | `System_Ext(defs, ...)` | file outside git | Read only by Definitions |
| Snapshot file / Issue tracker / Git hosting | `System_Ext(...)` | file / HTTPS / git | Collection's inputs; network only in Collection |

Containers inside one process sit in one `Container_Boundary(em, "Evidence Meter")`. Context packages are
drawn as containers because their boundaries are the architecture; `shared` and `platform` are not drawn.

## Conventions a SAD must respect (cite them in §2 and §8)

- Dependency rule: a context imports only itself, `shared`, `platform`; inward layers; Computation
  `domain` imports only the standard library and `shared` (`tests/test_architecture.py`).
- Contexts talk through events dispatched by `entrypoints/`; a cross-context call is a bc-map question.
- A refusal is a result (Verdict / Refusal with a code), not an exception.
- API errors: `{"error": {"code", "message"}}`.
- Migrations: `migrations/NNNN_<lower_snake>.up.sql` + `.down.sql`, applied by `platform/migrate.py`.
- Each context owns its tables, prefixed by its name, in the one SQLite file.
- Standard library first; a new dependency needs the owner's OK and a licence check.
- Synthetic data only in the repo; private codes, thresholds and state names in `~/.config/evidence-meter/`.
- Team-level only: nothing per person in outputs, records or logs.
- Commit subjects follow AGENTS.md (lesson id prefix in this repo); `make check` before each commit.

## Template rows that are usually the same

- §7 Deployment for a CLI-only feature: deliberate `<!-- N/A -->` with a one-sentence reason and a capacity
  note.
- §8 Authentication: none until a data-serving surface; then OIDC per repo ADR 0004.
- §8 Observability: none beyond tests for a local CLI.

## Checks (step 7)

Run each and record the result in the handoff.

1. **Inputs complete.** List every input of each stored value (snapshot, definition version, state map,
   thresholds, period rule). Each must be in the value's identity or stored with it, so a changed input
   gives a new record instead of a false "re-run differs".
2. **Refusal coverage.** Table: PRD error AC → refusal code (§8) → §6 branch or "added by
   complete-sequence-diagrams". No AC without a code, no code without an AC, and QG for all-or-nothing in
   §10 names every refusal AC.
3. **Event ledger.** For each touched context, the bc-map events it publishes or listens to: produced here,
   consumed here, or listed in §11 accepted debt with why.
4. **Privacy ledger.** Every place person data or private names could land (snapshot store, measurement
   rows, logs, terminal, repo files, test fixtures): "never" with the control, or "only here" with why that
   place is safe (gitignored, local).
5. **Diagram honesty.** In §6, every `alt`/`else` branch ends with its own reply to the actor; a reply
   after the last `end` (the lint warns) must hold for every branch, otherwise move it inside them.
