# Evidence Guard

Decides whether a computed value may be shown: enough data, enough coverage, no per-person breakdown. Its
output is a verdict with a reason, so a refused value is a result, not an error.

- **Terms:** Verdict, RefusalReason, Coverage, Threshold.
- **Publishes:** `ValueAccepted`, `ValueRefused`.
- **Listens to:** `MetricComputed`, `DefinitionVersionPublished`.
- **Structure:** handler/service/repo; move to domain/app/infra if the rules grow.
