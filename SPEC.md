# Evidence Meter v1 specification

What the first version must do and must not do. Sources: [README.md](README.md) (the idea) and
[docs/bc-map.md](docs/bc-map.md) (boundaries and events). Feature detail goes into
`docs/features/<slug>/PRD.md`; this page stays short.

## Goals

1. Collect issue tracker and Git data for one team and one period into an immutable snapshot.
2. Compute each metric from a versioned definition, so a value can be traced to the definition version
   and the inputs it used.
3. Refuse a value the data cannot support, with a reason a reader understands (too little data, low
   coverage, a per-person breakdown).
4. Draft a monthly page per team that a person reviews and publishes; refusals appear on the page.
5. Offer the same results through a CLI, a local API and a web page.

## Non-goals

- Any output, column or log line with a value per person. The tool must not become a ranking of people.
- Organisation-specific metric codes, thresholds or identifiers in the repository; they live in a
  private definitions file outside git.
- Hosting for several organisations, or a server reachable beyond localhost before sign-in exists.
- Editing tracker or Git data; the tool only reads.
- Real-time dashboards; the unit of reporting is a closed month.

## Key decisions

| Decision | Where |
|---|---|
| Python 3.12, FastAPI, argparse, SQLite; React + Vite + TypeScript web app | [ADR 0001](docs/adr/0001-stack.md) |
| Modular monolith, one package per context, imports checked by a test | [ADR 0002](docs/adr/0002-modular-monolith.md) |
| SQLite with plain SQL up/down migrations and a standard-library runner | [ADR 0003](docs/adr/0003-persistence-sqlite.md) |
| OIDC sign-in, provider from env, deferred to the first data-serving feature | [ADR 0004](docs/adr/0004-auth-oidc-deferred.md) |
| `status` split into `IssueState`, `Verdict`, `PageState` | [bc-map.md](docs/bc-map.md) |

## Acceptance criteria for v1

1. Given synthetic tracker and Git data for `team-alpha` and one month, collection stores a snapshot
   that later runs cannot change.
2. Every computed value names its definition id, definition version and the inputs it used.
3. Every metric has golden-data tests with expected values computed by hand.
4. A value below its minimum data or coverage is shown as refused with its reason, never as a number.
5. No output (CLI, API, page, log) contains a per-person value; a test checks each output.
6. The monthly page moves draft → reviewed → published, and only a reviewed page can be published.
7. Running with no private definitions file stops with a clear message and writes nothing.
8. `make check` passes offline on a clean clone after `make sync`.
