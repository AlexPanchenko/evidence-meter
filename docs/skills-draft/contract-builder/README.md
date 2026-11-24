# contract-builder (draft)

Own variant of the SDLC plugin's `api-forge` skill (homework m06-l06, hard level). The draft lives here
because Claude cannot write to `.claude/skills/`; the owner installs it:

    mkdir -p .claude/skills && cp -R docs/skills-draft/contract-builder .claude/skills/

Files: `SKILL.md` (flow; what changed against the plugin is at its end), `templates/cli.md` (exit-code
classes, checks-in-order table, output-field origins), `templates/events.md` (in-process events from
bc-map), `templates/openapi.yaml` and `templates/rules-openapi.md` (the repository's `{"error": {code,
message}}` envelope, 127.0.0.1 until OIDC), `templates/report.md`, `scripts/check_contract.py` (static
self-check, exit code).

`check_contract.py` was tried before the run: 0 findings on the plugin's F1 contract, 4 of 4 planted faults
on a broken copy (unknown refusal code, duplicate exit code, `# stale` under a PASS, a person field).

## Run: comparison with the plugin's api-forge

Same feature (`metric-computation`), same inputs, same four owner decisions. The plugin's skill, run in the
main session, gave [contracts/cli.md](../../features/metric-computation/contracts/cli.md) and
[api-sync-report.md](../../features/metric-computation/contracts/api-sync-report.md) (2,320 words, 21
origin rows, 3 deferrals), then the drift drill (rename a column, `--reconcile` FAIL with the field kept as
`# stale`, `git revert`, `--reconcile` PASS). contract-builder at easy depth, in a clean-context subagent
told not to open the plugin's output (an instruction, not a sandbox block), gave
[skill-run/contracts/](../../features/metric-computation/skill-run/contracts/) `cli.md`, `events.md`,
`contract-report.md` (4,022 words, 57 origin rows, 5 deferrals, 8 implied tests). Both: PASS (with
deferrals); `check_contract.py` 0 findings.

What I added or removed, and where it paid off:

1. I added a checks-in-order table for every command, and exit-code classes instead of one code per branch.
   The biggest gain is in the error replies: the import command got its own ordered checks, and the order
   is something a test can verify.
2. The privacy point (drift check 6) found something the plugin run missed. SAD §8 says stderr never
   carries a team id or state name, but AC-02, AC-04 and AC-07 need those in the Lead's terminal reply.
   That is now an item in task T12.
3. I removed the HTTP defaults that F1 cannot use: BearerAuth, `/api/v1`, Idempotency-Key and cursor
   pagination. Pagination therefore brings no gain here; it stays in the HTTP template for the first route
   that serves data.
4. I reworked the plugin's step 5 (errors from sequences) for a CLI. Refusal codes are checked against the
   ADR file and are not remembered, and a code the flows need becomes a proposal row.
5. Cost: the skill's output is about 1.7 times longer. 36 of its extra origin rows trace output text and
   flags one by one. That suits an audit and is heavy for a first read; `--depth easy` should probably keep
   only one row per field.

Fixed after the run (from the subagent's notes): the checker looked for `adr/` only beside the contracts
folder, so an `--out-dir` run failed with 6 false findings (it now walks up to the nearest `adr/`). It read
only the first "Checks, in order" table (it now reads all of them; a planted code in the second table is
caught). I also defined `--depth` and "flag", allowed framework defaults as an origin, replaced "one
command per story" with grouping, and put the `cli.md` template's frontmatter first.
