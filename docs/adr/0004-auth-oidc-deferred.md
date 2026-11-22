---
status: Accepted
date: 2026-11-22
---

# ADR 0004: Auth — OIDC with the provider from configuration, deferred to the first data-serving feature

## Context and problem statement

The backend and web app will show team metrics, which must not be open to anyone on a network. The owner
asked whether to add Google Workspace sign-in from the start.

## Decision drivers

- The repository is public: client ids, secrets and an organisation's domain must stay outside git.
- `make dev` must work on a clean clone without credentials.
- The skeleton serves no data yet (`/health` only).

## Considered options

1. OIDC, provider from env (Google Workspace as the first provider), implemented with the first feature
   that serves data; bind to 127.0.0.1 until then.
2. Google sign-in in the scaffold.
3. A static bearer token on every route now.

## Decision outcome

Option 1. Generic OIDC keeps the code provider-neutral; the issuer, client id, secret and allowed domain
come from env (names in `.env.example`, values only in a private `.env`).

### Consequences

- Good: no auth code guarding nothing; no organisation identifiers in the repository.
- Bad: the API must not be exposed beyond localhost until the auth feature ships; any change to the bind
  address waits for it.
