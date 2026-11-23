---
status: Draft
owner: "<feature owner role>"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "<today YYYY-MM-DD>"
feature_size: "<from .size: XS/S/M/L/XL>"
contexts: ["<context that owns the feature>", "<context it hears from, if any>"]
skill: prd-builder
ticket: "<id or none>"
---

# PRD — <slug>

<!-- Skill instruction: one-line links to inputs used.
> **Inputs (required):** [idea-brief](./idea-brief.md) · [CONTEXT](./CONTEXT.md)
> **Reference module:** `<path>` — patterns used (idempotent repeat, all-or-nothing, refusal lists the offending items, ...). None → «N/A — green-field».
> **Other channels used:** project docs by path (SPEC.md criteria by number, docs/bc-map.md, ADRs), or «None».
Never name a private definitions file's contents, an organisation, a person or an internal URL. -->

## 1. Context

<!-- Skill instruction: 3-4 paragraphs, WHAT + WHY, no stack names (see references/repo-patterns.md banned list).
¶1 Problem and who has it (idea-brief §2, §3). ¶2 Why now (idea-brief §4). ¶3 Committed approach, cited from
idea-brief §13 by name. ¶4 Traceability bullets: reference patterns → which AC/NFR they shaped; owner decisions
from the deep-dive; critic outcomes («Critic pass: ...», «Decision override: <headline> — rationale: <reason>»). -->

## 2. Goals

<!-- Skill instruction: 2-3 outcomes, no numbers (numbers live in §7). One of them is always about trust:
a value can be traced and recomputed. -->

## 3. Non-goals

<!-- Skill instruction: 3-6 bullets «<what> — <reason>». Sources: idea-brief §6 and §14 (parked approaches).
Always include, when the feature produces values: «Any value, column or log line per person — the tool must
not become a ranking of people». If the decision belongs to another context, name the context. -->

## 4. User stories

<!-- Skill instruction: ≥5, roles ONLY from the CONTEXT glossary. Title = 3-6 word action.
A story about «learning why nothing was produced» only gets refusal or error ACs; a story that produces
a value gets result ACs. -->

### US-01: <action title>
**As a** <glossary role>
**I want** <action>
**So that** <observable benefit>

## 5. Acceptance criteria

<!-- Skill instruction: Given/When/Then, business-observable, ≥1 of each coverage type
(happy / error / authorization / domain invariant / cross-context) and ≥1 per US.
Heading: «### AC-NN (US-XX) — <coverage type> · <outcome class>», outcome class is one of:
- result — the system records and shows something (a value, or a stated «no value» such as an empty median);
- refusal — a value exists but may not be shown; the reason is a Verdict from Evidence Guard, never an error;
- error — the system stops, records nothing, tells the actor what to fix; gets a code in §10.
Edge cases are AC-NNb. Zero tokens from the forbidden list (HTTP verbs, URL paths, status numerics,
`context.error_name` strings, JSON fragments, SQL constructs) — codes live in §10, not here.
Where «zero» could be misread, the Then says «shows no number and no zero» explicitly. -->

### AC-01 (US-01) — happy path · result
**Given** <business preconditions, synthetic names: team-alpha, 2026-10>
**When** the <role> <action>
**Then** the system <records / shows ...>

## 6. Non-functional requirements

<!-- Skill instruction: start from the defaults in references/repo-patterns.md («NFR defaults»), keep the rows
that apply, change targets only with a reason in §1 ¶4. Every row numeric with a measurement the repo can run
(a test in `make check`, a timed CI test). A row that does not apply now is kept with target «N/A — <reason>»,
so the next feature sees it was considered. -->

| Aspect | Target | Measurement |
|---|---|---|
| <Run time for one team and period> | ≤ <N s> for <N> issues | timed test on a synthetic snapshot |
| Reproducibility | 100% identical value and inputs on re-run | re-run test over golden data |
| Offline | 0 network calls | test with network blocked (SPEC 8) |
| Per-person data | 0 per-person fields in outputs, records, logs | output scan test (SPEC 5) |
| All-or-nothing | 0 partial records after any error AC | store-unchanged test per error AC |
| API read latency p95 | <≤ N ms on 127.0.0.1, or N/A — no API surface> | timed API test |
| Availability / throughput | N/A — local single-user tool until sign-in (ADR 0004) | — |

## 6.1 Security / privacy

<!-- Skill instruction: classification (one word + why); personal data the inputs may carry and what the
feature reads from it; authZ impact (local only until ADR 0004 changes); 3-5 abuse cases with the business
response; security review Required for M+ or any new boundary around person data. -->

## 7. Metrics / KPIs

<!-- Skill instruction: ≥3, baseline → target → timeframe. A baseline that is estimated says «estimated» and
gets a §8 row to measure it. Always one KPI for the lead's time per unit of work and one for refusals/errors. -->

## 8. Open questions

<!-- Skill instruction: `- [ ] <question>? Default now: <X>. — owner: <role>, due: <date or stage>`.
No row without owner and due. -->

## 9. Data and people

<!-- Skill instruction (prd-builder addition): answers, in this order —
1. Which inputs can identify a person (assignee, author, reviewer) and whether the feature reads them.
2. What the feature outputs, at which level (team, period); confirm «no value per person» for every surface:
   command output, stored record, log line, page, API.
3. Small-team rule: from what team size a team value is effectively personal, and which context decides
   (default: Evidence Guard; F-level «no limit» must be stated, not implied).
4. Synthetic data used in tests and examples (team-alpha, team-beta; never a real team or project key).
5. Private definitions: what is read at run time from outside git, and that none of it is copied into the repo. -->

## 10. Errors and refusals

<!-- Skill instruction (prd-builder addition): one row per error or refusal AC. Codes follow
`<context>.<error_name>`, snake_case, context from docs/bc-map.md (collection, definitions, computation,
evidence_guard, reporting). Errors leave the API as {"error": {"code", "message"}}. A refusal is NOT an
error: it has no code here, only the Verdict reason Evidence Guard returns. -->

| AC | Outcome class | Code or Verdict reason | Message the actor sees | Records anything? |
|---|---|---|---|---|
| AC-NN | error | `<context>.<error_name>` | <plain sentence> | no |
| AC-NN | refusal | Verdict: <reason> | <plain sentence> | the Verdict only |

## 11. States and events

<!-- Skill instruction (prd-builder addition): only the states and events this feature touches, from
docs/bc-map.md. List allowed transitions as «from → to (event)»; name a forbidden transition when an AC covers
it. «N/A — the feature changes no state» is valid. Never reuse the word «status» across contexts: IssueState
(Collection), Verdict (Evidence Guard), PageState (Reporting), DefinitionVersion published/retired (Definitions). -->

| Object (context) | Transition | Event | AC |
|---|---|---|---|
| <object> (<context>) | <from> → <to> | `<EventName>` | AC-NN |
