<!-- contract-builder template: copied to contracts/events.md when the feature publishes an event.
     Events are in-process (entrypoints/ dispatcher); names come from docs/bc-map.md, not invented. -->
# Events — <slug>

| Event (bc-map name) | Published by | When | Not published when | Listeners now |
|---|---|---|---|---|
| `<EventName>` | <context, command> | <§6 step> | <no-op branch> | <none yet / context> |

## `<EventName>`

| Field | Type | Origin | Private name? |
|---|---|---|---|
| `<field>` | <type> | <table.column> | <yes: in process only, never logged / no> |

- Payload holds no person field and is never written or logged (SAD §8 privacy ledger).
- Additive only: a new field is fine; a rename is a new event name in bc-map.
