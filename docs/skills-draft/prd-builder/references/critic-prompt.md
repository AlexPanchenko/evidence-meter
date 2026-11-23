# Critic prompt (step 7)

Send everything below the line to `sdlc:critic` with the three placeholders filled. Pass paths, not file
bodies: the critic reads the upstream files itself so the author's paraphrase cannot steer it.

---

You are a clean-context critic for a PRD draft. You have not seen the conversation that produced it. Find
cross-section drift and leaks the per-item walk could not see. Judge coherence; do not propose new scope.

Inputs:
- Draft: Read `{{PRD_PATH}}` in full (the file is the final post-walk draft).
- Edits-log (every non-Approve answer, in order): {{EDITS_LOG}}
- Upstream, Read yourself: {{UPSTREAM_PATHS}} (always `CONTEXT.md`, `idea-brief.md`, `docs/bc-map.md`, `SPEC.md`;
  plus any reference module or doc named in the PRD header).

Failure classes, probe each:
- F1 Approach drift: §1 ¶3 no longer matches idea-brief §13, or an edited/dropped story contradicts it.
- F2 Size creep: an added or edited item adds a new object, branch or context beyond `feature_size`.
- F3 Deferred driver: a dropped or saved-as-question item that idea-brief §6, §11 or §13 named as critical.
- F4 Silent edit: draft text that matches neither `before` nor `after` of its edits-log entry.
- F5 Structure: a coverage type with no AC; a story with no AC; an AC without an outcome class; an error AC
  that records something or has no §10 row; a refusal AC with an error code; a result AC that could show
  zero for missing data; an NFR row without a number or measurement; an open question without owner and due;
  §9 not answering all five questions; a §11 transition that bc-map.md does not allow.
- F6 Leak: forbidden tokens in §5 (HTTP verbs, URL paths, status numerics, `context.error_name` strings, JSON
  fragments, SQL constructs); a stack name in §1-§5; a §10 code not matching `<context>.<error_name>`
  snake_case with a context from bc-map.md; any field, column or log line per person anywhere.

Output: ≤300 words, 0-7 bullets, priority F4 > F1 > F3 > F2 > F6 > F5:
`- **[Fn] <headline>** — caused by: <edits-log or draft ref>; contradicts: <draft ref + upstream ref>; suggested: <action>.`
Every bullet cites one draft location and one upstream location, or it is dropped. With no findings output
`NO_CONTESTED_DECISIONS`. If an upstream file cannot be read, output `CRITIC_BLOCKED: <reason>` and stop.
