---
paths:
  - "tests/**/*.py"
---

# Tests

- Test behaviour through the public interface, not private helpers, so a refactor that keeps behaviour
  keeps the tests green.
- Every fixture value is invented: team, project, person and metric code names that cannot be mistaken for
  a real organisation's (for example `team-alpha`, `PRJ-DEMO`, `metric-x`). The tests are published with
  the code.
- Golden data for a metric sits next to its test with the expected value computed by hand and a one-line
  comment showing the arithmetic. Never generate the expected value with the code under test.
- One rule, one test: when a list of rules must hold (permissions, sandbox, refusals), parametrize over the
  list so a failure names the rule that broke.
- The settings tests read `.claude/settings.json` through the `settings` fixture in `tests/conftest.py`;
  a new control in the settings gets a test there in the same commit.
- A test that needs the network, the clock or a real file outside the repository gets a fake or
  `tmp_path` instead; `make check` must pass offline and inside the sandbox.
