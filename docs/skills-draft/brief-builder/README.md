# brief-builder (draft)

Own variant of the SDLC plugin's `interview` skill (homework m06-l02, hard level). The draft lives here
because Claude cannot write to `.claude/skills/`; the owner installs it:

    mkdir -p .claude/skills && cp -R docs/skills-draft/brief-builder .claude/skills/

(`mkdir -p` first: without it, the first `cp -R` makes the skill folder itself become `.claude/skills/`.)

## Run 2026-11-23: comparison with the plugin's interview

Same feature (`metric-computation`): the plugin's interview at hard depth gave
[idea-brief.md](../../features/metric-computation/idea-brief.md) (2144 words, 4 sub-agents, about 12
checkpoints); brief-builder at easy depth gave
[idea-brief.brief-builder.md](../../features/metric-computation/idea-brief.brief-builder.md) (1159 words,
3 checkpoints, no sub-agents).

- Added: §16 Data and people and §17 Evidence of the pain; a status-quo row and fetched/snippet marks in
  §6; Reach in units of work; four standard failure modes for the devil's advocate; English questions with
  offered wordings for the raw idea.
- Biggest gain: the per-person question and the measured-or-estimated question are asked on every run, so
  the two risks that matter most for a metrics tool are written down, not left to the devil's advocate.
- Reworked step: the raw-idea capture (offered wordings instead of a blank prompt) and the RICE batch
  (units of work, owner changes recorded).
- The plugin's run was more thorough: verified competitor pages and independent sub-agent views. The easy
  run reused approaches and the matrix from the same session, so it is not an independent second opinion.
- Changed in SKILL.md after the run: an exact easy route, `--out` for comparison runs, and "run in a fresh
  session when a brief for the slug is already in context".
