# Architecture

Modular monolith: one Python package per bounded context, wired only by the entry points. The full map
is [docs/architecture-map.md](docs/architecture-map.md); boundaries, events and glossary are in
[docs/bc-map.md](docs/bc-map.md); the reasons are in [docs/adr/](docs/adr/).

## Layout

| Path | What lives there |
|---|---|
| `src/evidence_meter/<context>/` | One context: `collection`, `definitions`, `computation`, `evidence_guard`, `reporting` |
| `src/evidence_meter/shared/` | Shared kernel: `Team`, `Period`, event types; no context logic |
| `src/evidence_meter/platform/` | Technical helpers: configuration from env, SQLite access, migration runner |
| `src/evidence_meter/entrypoints/` | `cli.py` (argparse) and `api.py` (FastAPI): the only place that wires contexts |
| `migrations/` | `NNNN_<name>.up.sql` and `.down.sql`, applied by `make migrate` |
| `web/` | React + Vite + TypeScript app; calls the API under `/api` |

Structure inside a context: Computation is `domain/` → `app/` → `infra/`; the other four are
`handler/` → `service/` → `repo/`.

## Dependency rule

- A context imports only itself, `shared` and `platform`. Never another context, never `entrypoints`.
- `shared` and `platform` import no context and no entry point.
- Inside a context, imports point inward: `handler` → `service` → `repo`; `infra` → `app` → `domain`.
- Computation's `domain` imports only the standard library and `shared`: formulas stay pure, no I/O.
- Contexts talk through events; `entrypoints` dispatches them. `tests/test_architecture.py` enforces all
  of this in `make lint`.

## Where logic lives

- A metric formula: `computation/domain/`, with golden data in `tests/` (expected values by hand).
- Whether a value may be shown: `evidence_guard/`. A refusal is a `Verdict` with a reason, not an error.
- Reading the tracker or Git: adapters in `collection/repo/`.
- The private definitions file: read only by `definitions/`.
- Page draft, review, publication: `reporting/`. Team-level only, never a value per person.
- API errors: `{"error": {"code", "message"}}`, set in `entrypoints/api.py`.

## Events: who publishes, who listens

| Event | Published by | Listened to by |
|---|---|---|
| `ReportingPeriodClosed` | external trigger (CLI or scheduler) | Collection |
| `TrackerSnapshotCollected`, `GitHistoryCollected` | Collection | Computation |
| `CollectionFailed` | Collection | Reporting |
| `DefinitionVersionPublished` | Definitions | Computation, Evidence Guard |
| `MetricComputed` | Computation | Evidence Guard |
| `ValueAccepted`, `ValueRefused` | Evidence Guard | Reporting |
| `PageDrafted`, `PageReviewed`, `PagePublished` | Reporting | nobody yet |

## Runtime

The API and the web dev server bind to 127.0.0.1 only until OIDC sign-in ships with the first feature
that serves data ([ADR 0004](docs/adr/0004-auth-oidc-deferred.md)). SQLite file from `EVIDENCE_METER_DB`.
