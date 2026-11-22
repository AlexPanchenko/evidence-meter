---
paths:
  - "src/evidence_meter/evidence_guard/**"
---

# Evidence Guard context

- A refusal is a `Verdict` with a `RefusalReason`, returned as a result and published as `ValueRefused`;
  never raise an exception for "not enough data".
- Every rule says why in its reason, in words a reviewer can check against the data (coverage, sample
  size, missing source).
- Team-level only: refuse any value that would show or let someone derive a result per person, and never
  log a value per person.
- Thresholds come from the definition version at run time (`DefinitionVersionPublished`); none is
  hard-coded, and none is copied from the private definitions file into code or tests.
- The guard reads computed values and definitions; it does not recompute a formula or read the tracker.
