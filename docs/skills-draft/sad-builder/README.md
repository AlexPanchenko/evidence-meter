# sad-builder (draft)

Own variant of the SDLC plugin's `architecture-design` skill (homework m06-l04, hard level). The draft lives
here because Claude cannot write to `.claude/skills/`; the owner installs it:

    mkdir -p .claude/skills && cp -R docs/skills-draft/sad-builder .claude/skills/

Files: `SKILL.md` (flow), `templates/sad-template.md` (Arc42 with a context touch list, an event ledger and
repo rows in §8), `templates/adr-template.md` (context-prefixed names, 4-tick gate score, stored-data
consequences), `references/gate.md` (4 criteria), `references/repo-patterns.md` (recommended containers,
conventions, step-7 checks), `references/c4-mermaid-syntax.md` (ported, repo examples),
`references/critic-prompt.md`, `scripts/lint_mermaid.py` (structural lint; `mmdc` cannot run in the sandbox).

What changed against the plugin is listed at the end of `SKILL.md`.

## Run: comparison with the plugin's architecture-design

Same feature (`metric-computation`): the plugin's architecture-design at medium depth gave
[sad.md](../../features/metric-computation/sad.md) with 8 ADRs (3776 words; the critic found 6 issues, among
them the state map missing from the measurement key); sad-builder at easy depth, in a fresh session that did
not read the plugin's SAD, gave [sad-builder/sad.md](../../features/metric-computation/sad-builder/sad.md)
with 9 context-prefixed ADRs (4208 words). Both reached the same strategy (CLI only, entrypoint
orchestration, file import, person fields dropped at import, UTC months, typed refusals), so the difference
is in the details the plugin left to its critic.

I added a 4th gate criterion (stored data), context-prefixed ADR names, §5 from recommended containers
with a context touch list, event and privacy ledgers and five repo checks before the critic, and removed
the plugin's shared files and fixed-Ukrainian questions. §5 gained most from the touch list (every part,
table prefix, event and migration F1 changes in one table); §6 gained more: flow 2 covers all six refusal
ACs in a fixed order with a reply per branch, and the measurement key holds every input (version hash,
state-map hash) from the first draft, where the plugin needed its critic. The step I reworked is the
coherence check: deterministic repo checks now run before the critic, and they also caught that team ids
and issue keys are private names. The costs: the stored-data criterion made the TOML-format choice an ADR
the plugin kept inline, the shared kernel widened (a §1 override and a docs update), and the two SADs
disagree on whether an AC-03 mismatch is a refusal code or a defect, to settle before api-forge. For this
repository's practice sad-builder's SAD is the closer fit.

## Changed after the run

Nothing yet.
