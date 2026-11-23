---
status: Living
updated_at: "2026-11-23"
---

# Domain Context — metric-computation

Feature glossary for F1. Context-level terms and their owners are in [docs/bc-map.md](../../bc-map.md);
this file fixes the words the F1 artifacts use, with the concept each one gets confused with.

## Glossary

- Cycle time — the median duration of the passes a team finished in a period, each pass measured from its start to its done. NOT lead time, which runs from the request (issue created) or the first commit, not from the start of work.
- DefinitionVersion — an immutable, numbered version of a metric definition that names its formula, its inputs and its minimum data. NOT MetricDefinition, which is the named metric across all its versions.
- Formula — a pure function, named by a FormulaId, that turns inputs into a value without reading or writing anything. NOT DefinitionVersion, which names a formula and its inputs as data; the formula itself is code.
- Input — a named value read from one snapshot that a formula consumes, for example the count of issues closed in the period. NOT Snapshot, which is the whole immutable collection the input is read from.
- Lead — the person who runs the monthly computation for the teams they are responsible for and reviews the values before the page is drafted. NOT a team member being measured: the tool reports on the team, never on the lead or any other person.
- Measurement — the raw value computed for one team, one period and one definition version, together with the inputs it used. NOT a value that may be published: a measurement goes on a page only after Evidence Guard returns a Verdict; before that only the lead sees it, marked as not yet checked. When no passes were finished in the period, a measurement has no value (the median is not defined); it never becomes zero.
- Pass — one stretch of work on an issue from a start (first start, or a reopen) to the next done; a reopened issue has several passes, each counted in the period of its own done. NOT Issue, which can have one or more passes.
- Period — a closed calendar month for which values are computed, identified as YYYY-MM. NOT a sprint or iteration from the tracker, whose dates vary by team.
- State map — one team's mapping from its tracker states to the abstract states a definition version uses (started, done, excluded), kept in the private definitions file. NOT IssueState, which is the state an issue actually has in the tracker.

## Invariants

- A Measurement always names its definition id, its definition version and the inputs it used ([SPEC.md](../../../SPEC.md), acceptance criterion 2).
- A Measurement is always for a team, never for a person ([SPEC.md](../../../SPEC.md), non-goals).
