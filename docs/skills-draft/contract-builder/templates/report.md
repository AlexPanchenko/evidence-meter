# contract-report — <slug>

**Verdict:** PASS | PASS (with deferrals) | FAIL
**Run:** <date> (run <N>, first run | --reconcile) · **Scenario:** A | B
**Sources read:** PRD ✓ · sad.md §6 ✓ · data-model ✓/✗ · refusal ADR ✓/✗ · CONTEXT ✓/✗
**Contract:** <cli.md | openapi.yaml | events.md> · **Self-check:** `check_contract.py` exit <0|1>

## Field origins

| path | origin | confidence |
|---|---|---|

Dropped for lack of an origin: <template fields, or "none">.

## Drift check

1. Command ↔ data-model *(core)* — ✓ | ✗
2. Refusal code ↔ ADR closed list *(core)* — ✓ | ✗
3. Constraint ↔ column *(core)* — ✓ | ✗
4. Coverage *(supporting)* — ✓ | ✓ (deferred: …) | ✗
5. Flow branches *(supporting)* — ✓ | ✓ (deferred: …) | ✗
6. Privacy *(core)* — ✓ | ✗

## Owner decisions

| Flag | Action | Result |
|---|---|---|

## Unresolved origins

None (scenario A) | <path · current origin · what reconcile tightens>

## Tests the contract implies

- <one per checks-in-order row and per exit-code class>

## Deferrals

| What | Why parked | Next step |
|---|---|---|
