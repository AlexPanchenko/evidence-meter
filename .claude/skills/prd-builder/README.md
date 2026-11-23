# prd-builder (draft)

Own variant of the SDLC plugin's `write-prd` skill (homework m06-l03, hard level). The draft lives here
because Claude cannot write to `.claude/skills/`; the owner installs it:

    mkdir -p .claude/skills && cp -R docs/skills-draft/prd-builder .claude/skills/

Files: `SKILL.md` (flow), `templates/PRD-template.md` (11 sections + 6.1), `references/repo-patterns.md`
(contexts and states, refusal as Verdict, error-code convention, NFR defaults), `references/critic-prompt.md`.

## Run 2026-11-23: comparison with the plugin's write-prd

Same feature (`metric-computation`): the plugin's write-prd at hard depth gave
[PRD.md](../../features/metric-computation/PRD.md) (1886 words, 7 stories, 11 ACs, critic 3 findings);
prd-builder at easy depth, in a fresh session, gave
[PRD.prd-builder.md](../../features/metric-computation/PRD.prd-builder.md) (3214 words, 6 stories,
15 ACs, critic 4 findings, all self-checks clean).

Added §9 Data and people, §10 Errors and refusals with `<context>.<error_name>` codes, §11 States and
events, an outcome class (result / refusal / error) on every AC and NFR defaults with explicit N/A rows;
removed the roadmap step and the dependence on the plugin's shared files. The AC gain is largest where
write-prd left behaviour implied: the happy path now carries hand-checkable numbers (median 4.0 of 2, 3, 5
and 10 days), a re-run on a newer snapshot with different inputs became its own error (AC-11) instead of
"report a defect", and every error AC states that it records nothing and has a code. The reworked step is
the draft (step 5): §5 is drafted with the outcome class first, so the AC-01b drift the plugin's critic had
to catch (a recorded "no value" filed under a refusal story) could not recur. The cost is length (+70%)
and, at easy depth, five assumptions the owner did not confirm one by one; for this repository's practice
prd-builder's PRD is the closer fit.

## Changed after the run

Nothing yet.
