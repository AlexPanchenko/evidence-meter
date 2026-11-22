---
paths:
  - "src/evidence_meter/computation/**"
---

# Computation context

- `domain/` imports only the standard library and `shared`: no I/O, no clock, no environment, no other
  context. A formula is a pure function of a snapshot and a definition version, so golden data proves it.
- Every formula gets golden data in `tests/` with the expected value computed by hand and the arithmetic in
  a comment; never derive the expected value by running the formula.
- A Measurement keeps the inputs it used, so a reviewer can redo the arithmetic.
- Values are team-level only. No formula groups, sorts or returns values by person.
- Whether a value may be shown is not decided here: Computation publishes `MetricComputed` and Evidence
  Guard decides. Do not add thresholds or refusal logic to a formula.
- Formula ids and inputs come from the definition version at run time; never copy a metric code or a
  threshold from the private definitions file into code or tests.
