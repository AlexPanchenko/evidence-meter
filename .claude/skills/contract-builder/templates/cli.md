---
status: Draft
owner: "<owner>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: <XS|S|M|L|XL>
---

<!-- contract-builder template: copied to docs/features/<slug>/contracts/cli.md when sad.md
     target_surfaces includes cli. Every row needs an origin in contract-report.md; delete any row
     that has none. Synthetic values only. -->

# CLI Contract — <slug>

Derived from PRD §4-§5, sad.md §6 and §8, data-model.md and the refusal ADR. Origins and drift check:
[contract-report.md](contract-report.md).

## Global flags

| Flag | Short | Type | Description |
|---|---|---|---|
| `--help` | `-h` | bool | Print usage and exit 0. |
| `--version` | | bool | Top-level only: print the program version and exit 0. |

## Exit codes (all commands)

| Code | Class | Meaning | Origin |
|---|---|---|---|
| 0 | success | <done, or an idempotent no-op> | <flow, branch> |
| 1 | unexpected error | traceback on stderr, nothing recorded | SAD §8 Transactions |
| 2 | usage error | bad arguments | <refusal ADR> |
| 3 | refusal | nothing recorded; `Refused: <code>: <reason>` on stderr | <flow, branches> |
| 4 | defect | <an invariant broke, e.g. a re-run differs> | <AC> |

Refusal codes (closed list, <refusal ADR>): `<code>`, ... Proposals not yet in the ADR: `<code>` (Deferral).

## Command: `<binary> <command>`

<One line: the user story this serves.>

### Usage

```
<binary> <command> <arg> --<flag> <value>
```

### Arguments and flags

| Name | Required | Type | Default | Origin |
|---|---|---|---|---|
| `<arg>` | yes | <type, format> | | <column or AC or §6 message> |

### Checks, in order, all before the first write

| # | Check | Refusal code (exit 3) | Reply on stderr | Origin |
|---|---|---|---|---|
| 1 | <cheapest, no I/O> | `<code>` | <plain reason> | <AC, flow branch> |

### Output (exit 0, stdout)

```
<synthetic example: team-alpha, 2026-10, <sha256>>
```

| Output field | Origin |
|---|---|
| <field> | <table.column or AC> |

Nothing in any output identifies a person.

## Backwards-compat policy

Additive only. Removing or renaming a flag, a refusal code or an exit-code meaning is breaking.
