# C4 Mermaid syntax for §3 and §5

Ported from the plugin's cheatsheet, with examples from this repository. L1 Context goes in §3, L2 Container
in §5; L3 and L4 are out of scope.

## L1 — System Context (`C4Context`, §3)

The system as one box, its people and the external systems this feature touches. 4-8 elements.

```mermaid
C4Context
    title Evidence Meter (metric-computation) — System Context

    Person(lead, "Lead", "Runs the monthly computation for their teams")
    System(em, "Evidence Meter", "Computes team metrics from versioned definitions")
    System_Ext(snap, "Snapshot file", "One team's issue history for a closed period")
    System_Ext(defs, "Private definitions file", "Definition versions and state maps; outside git")
    System_Ext(tracker, "Issue tracker", "Not connected in this feature")

    Rel(lead, em, "Imports snapshots, computes", "CLI")
    Rel(em, snap, "Imports once", "file read")
    Rel(em, defs, "Reads at run time", "file read")
    Rel(em, tracker, "Reads issues (later feature)", "HTTPS")
```

Elements: `Person`, `Person_Ext`, `System`, `System_Ext`, `SystemDb`; `Rel(from, to, "what", "how")`.

Rules:
- Contexts (Collection, Computation, …) never appear in L1; they are L2.
- Use glossary role names (`Lead`), never `User` or `Admin`.
- A system the feature does not connect yet is drawn with "(later feature)" or left out; never implied.

## L2 — Container (`C4Container`, §5)

One process, so one `Container_Boundary`; context packages are containers because their boundaries are the
architecture. `shared` and `platform` are not drawn. Start from the recommended containers in
[repo-patterns.md](repo-patterns.md).

```mermaid
C4Container
    title Evidence Meter (metric-computation) — Containers

    Person(lead, "Lead", "Runs the monthly computation")

    Container_Boundary(em, "Evidence Meter") {
        Container(cli, "CLI (entrypoints)", "Python, argparse", "Commands; orchestrates a run")
        Container(collection, "Collection", "Python package", "Imports and stores snapshots")
        Container(computation, "Computation", "Python package", "Pure formula; records measurements")
        ContainerDb(db, "Local database", "SQLite", "collection_* and computation_* tables")
    }

    System_Ext(defs, "Private definitions file", "TOML outside git")

    Rel(lead, cli, "Runs commands", "terminal")
    Rel(cli, collection, "Get snapshot", "function call")
    Rel(cli, computation, "Compute with mapped inputs", "function call")
    Rel(collection, db, "Reads and writes collection_*", "sqlite3")
    Rel(computation, db, "Reads and writes computation_*", "sqlite3")
```

Elements: `Container_Boundary(id, "label") { … }`, `Container`, `ContainerDb`, `ContainerQueue` (none in this
repo yet); `Person` and `System_Ext` reused from L1.

Rules:
- One container per declared `target_surface` (CLI, API, web).
- No arrow from one context to another: wiring goes through `entrypoints` (dependency rule). If a diagram
  needs one, it is a bc-map question, not a drawing choice.
- Label every arrow with what and how (function call, sqlite3, HTTPS, file read).

## Two surfaces (CLI + API + web)

```mermaid
C4Container
    title Evidence Meter (reporting) — Containers

    Person(lead, "Lead", "Reviews and publishes the monthly page")

    Container_Boundary(em, "Evidence Meter") {
        Container(web, "Web app", "React, Vite, TypeScript", "Monthly page; calls /api")
        Container(api, "Backend API (entrypoints)", "Python, FastAPI", "Owns the JSON contract; OIDC")
        Container(reporting, "Reporting", "Python package", "Page draft, review, publication")
        ContainerDb(db, "Local database", "SQLite", "reporting_* tables")
    }

    Rel(lead, web, "Reviews pages", "HTTPS")
    Rel(web, api, "Calls", "JSON over HTTP")
    Rel(api, reporting, "Page commands", "function call")
    Rel(reporting, db, "Reads and writes reporting_*", "sqlite3")
```

## Common mistakes

- `Container_Bondary` or `ContainerBoundary`: Mermaid draws an empty box without an error.
- A `Rel` to an element not declared above it.
- An arrow with no label or protocol.
- Mixing levels: a class or function inside an L2 diagram.

## Validating before commit

`mmdc` needs Chromium, which cannot start in the agent sandbox; CI runs `make diagrams`. In the session run
the structural lint, which catches the mistakes above for C4 and sequence diagrams:

```bash
python3 -I .claude/skills/sad-builder/scripts/lint_mermaid.py docs/features/<slug>/sad.md
```

Exit 0 means every block passed; otherwise it names the block and the problem. Say in the handoff that the
diagrams were linted, not rendered.
