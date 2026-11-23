---
name: sdlc-audit
description: Read-only inspection of one feature's SDLC artifacts. Scans docs/features/<slug>/ for the nine module 6 artifacts (CONTEXT, idea-brief, PRD, sad, adr/, data-model, openapi.yaml, api-sync-report, tasks/), marks each present, missing, stale or n/a with the reason, and ends with 3-5 recommendations for the most critical gaps. Use when the owner says "audit <slug>", "what is missing for <slug>", "sdlc status of <slug>" or "/sdlc-audit <slug>". Writes nothing unless --out is given.
---

# sdlc-audit

An inspection skill, not a workflow skill: it never creates or edits an artifact. It answers one question:
how far is this feature through the gates, and which document is missing or out of date?

## Inputs

- `<slug>`: a folder under `docs/features/`. Missing → list the folders and ask which one.
- Optional `--out`: also write the report to `docs/features/<slug>/_audit/sdlc-audit-<YYYY-MM-DD>.md`.

## The nine artifacts

| # | Artifact | Phase | Expected path (under `docs/features/<slug>/`) | Made by | Upstream (stale if older) | Code (stale if older) |
|---|---|---|---|---|---|---|
| 1 | CONTEXT | 1 idea | `CONTEXT.md` | `fix-term`, interview | — | — |
| 2 | idea-brief | 1 idea | `idea-brief.md` | `interview`, `brief-builder` | CONTEXT | — |
| 3 | PRD | 2 PRD | `PRD.md` | `write-prd`, `prd-builder` | idea-brief, CONTEXT | — |
| 4 | sad | 3 architecture | `sad.md` | `architecture-design` | PRD | the feature's contexts |
| 5 | adr/ | 3 architecture | `adr/NNNN-*.md` | `architecture-design`, `decide-adr` | sad | — |
| 6 | data-model | 4 contracts | `data-model.md` (+ staged `migrations/`) | `generate-data-model` | PRD, sad | the feature's contexts |
| 7 | openapi.yaml | 4 contracts | `contracts/openapi.yaml` | `api-forge` | PRD, data-model, sad | — |
| 8 | api-sync-report | 4 contracts | `contracts/api-sync-report.md` | `api-forge` | openapi, data-model | — |
| 9 | tasks/ | 5 code | `tasks/tasks.json` (legacy: `tasks.json`) | `break-tasks` | PRD, sad | the feature's contexts |

"The feature's contexts" come from the `contexts:` frontmatter of PRD.md (else sad.md), mapped to
`src/evidence_meter/<context>/`. None declared → code staleness is not checked, and the report says so.

## States

- **present**: the file or folder exists; the report adds its frontmatter `status` (Draft, Approved,
  Confirmed) and "uncommitted changes" when git shows any.
- **missing**: no file at the expected path. A repo-level stand-in (`docs/adr/` for adr/, `migrations/` for
  data-model) is named in the detail, but the feature-level artifact still counts as missing.
- **stale**: the artifact's last *content* commit is older than the last content commit of an upstream
  artifact or the last commit of the feature's code. A commit that changes only frontmatter lines (a status
  or date sync) is not a content change. Git commit times, never file mtimes (a checkout resets mtimes).
- **n/a**: not expected for this feature, with the reason. Only two reasons are valid: `sad.md` declares
  `target_surfaces` without an HTTP API (openapi.yaml → n/a; `contracts/cli.md` or `events.md` expected
  instead), or `.size` is XS/S and the size matrix makes the artifact optional (data-model when no storage
  changes). Without `sad.md`, nothing is n/a: the surface is undecided.

## Protocol

1. **Scan** (one command, show the output):
   `bash .claude/skills/sdlc-audit/scripts/scan.sh <slug>`
   It prints one TSV row per artifact and `#` context lines: size, contexts and last code commit, surfaces,
   variant files (`*.<name>.md` beside a canonical artifact), architecture-map staleness, PRD open questions.
2. **Read only what the scan points at**: the frontmatter of present artifacts; PRD §8 open questions whose
   due stage is the next missing phase; nothing else.
3. **Status table** in chat: `# · Phase · Artifact · State · Last commit · Detail`, then one line per `#`
   context line that matters (variants, a stale architecture map, undeclared contexts).
4. **Recommendations**, 3-5 lines, most critical first. Critical = the earliest phase with a missing or stale
   artifact, because every later artifact reads it. Each line: the gap, its consequence in one clause, and
   the command that closes it (for example `/sdlc:architecture-design <slug>`). Also flag: a variant file not
   reconciled with its canonical artifact; a stale architecture map before phase 3; a Draft PRD before
   phase 3; open questions due at the next phase; no `contexts:` in PRD or sad frontmatter (code staleness
   cannot be checked until it is added); a variant with more sections than its canonical artifact (content
   that exists only in the variant).
   End with the scan's "not visible" line: decisions held in chats, plans or tickets are outside the audit.
5. With `--out`, write the same table and recommendations to the report file; otherwise write nothing.

## Rules

- Read-only: no edits to artifacts, CONTEXT.md, code or git state.
- Report what the files say; never infer a phase as done from a chat, a plan or a commit message.
- Synthetic data only in the report; private definitions are never read.

## Definition of done

- Nine rows, each with a state and, for stale or n/a, the reason.
- Context lines shown for variants, contexts and the architecture map.
- 3-5 recommendations, each with a command.

## Changed after the first run (comparison with a manual inventory)

- Staleness ignores frontmatter-only commits → a brief whose status was synced in the same commit as a
  glossary change is now reported stale against the glossary, as the manual inventory found.
- Repo-level `migrations/` named as a stand-in for a missing data-model.
- Variant lines show sections and words for both files → an unreconciled variant with extra content stands out.
- Undeclared contexts and decisions held outside the repository are reported, not silently skipped.
