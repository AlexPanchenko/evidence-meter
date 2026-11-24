---
paths: ["docs/features/*/contracts/openapi.yaml", "src/evidence_meter/entrypoints/api.py"]
---

# OpenAPI rules (bootstrapped by contract-builder; the owner edits this file)

- OpenAPI 3.1.0; nullability as `type: [string, "null"]`.
- Errors: `{"error": {"code", "message"}}` as set in `entrypoints/api.py`; `code` from the feature's closed list.
- Refusal → 409 (state) or 422 (input); usage → 400; defect → 500.
- Lists: cursor pagination (`after`, `limit`), never offset.
- No auth scheme and 127.0.0.1 only until OIDC ships (docs/adr/0004).
- `$ref` for every shared schema; no inline duplicates.
- Banned: any field, parameter or example that names or counts a person; real team, project or state names in examples.
