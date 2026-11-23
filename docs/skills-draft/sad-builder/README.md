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

Not run yet. Plan: a fresh session runs `/sad-builder metric-computation --out-dir
docs/features/metric-computation/sad-builder/ --depth easy`; the comparison (3-5 sentences) goes here.

## Changed after the run

Nothing yet.
