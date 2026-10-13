# Payload tokens: uid, ref and the U+2024 separator

Author: Sayandip Bagchi.

---

## The allowed body

| Key | Value | Notes |
|---|---|---|
| `alertId` | registry alert ID, literal | a duplicated flow keeps its parent's value; re-check |
| `journey` | one of `config.json → journeys`, literal | same |
| `uid` | `{{UserAttribute['ID']}}` | the customer-ID user attribute; what it resolves to is tenant-specific (Q17) |
| `ref` | `{{EventAttribute['MOE_TRIGGER_EVENT․<event>․<attribute>']}}` | approved per alert (A0), listed in the tenant ref table |

Nothing else. No phone, email, name, amount, device, free text (security S5).

## The separator trap (Q18)

The dots inside the ref path are **U+2024 ONE DOT LEADER** (`․`), not U+002E FULL STOP (`.`).

```
wrong:  {{EventAttribute['MOE_TRIGGER_EVENT.<event>.<attribute>']}}   ← saves, reads back, resolves blank
right:  {{EventAttribute['MOE_TRIGGER_EVENT․<event>․<attribute>']}}
```

The two render almost identically in the UI and in screenshots. The only reliable checks:

- Insert through the personalisation picker, which writes the correct character.
- In the JS read-back, test the character, for example
  `[...bodyText].filter(c => c === '․').length === 2` for a ref token, and report the count.
- After go-live, the first intake row for the alert has a non-blank `ref` (A6a). A blank `ref`
  on a flow approved with one is a token defect until proven otherwise.

The registry, ref table and build logs **store** the path with ASCII dots
(`MOE_TRIGGER_EVENT.<event>.<attribute>`) by convention. Convert on the way into the connector;
never paste the stored form.

## What is personalisable (Q19)

Only attributes of the **trigger event** appear in the picker. Consequences:

- The ref must come from the trigger event, not the follow-up event and not an earlier event.
- Session-scoped identifiers are not in the picker. Flows whose only case identifier is
  session-scoped (for example, screen-view events) are **uid only by design**; record the reason in the
  tenant ref table and in the registry `notes`.
- If the approved ref is missing from the picker, the approval was for something unbuildable. Stop
  and return to `alert-design`; do not substitute another attribute.

## uid resolution (Q17)

`{{UserAttribute['ID']}}` resolves to whatever the tenant stores as the user ID: a customer UUID in
some tenants, MoEngage's own 24-hex ID in others. Record which in the tenant profile once the first
intake row arrives (length and format only, never the value), because investigators join on it.

## Reporting tokens

Reports and logs show token **templates** and "present / blank" for resolved values. A resolved
uid or ref value never appears in a report, capsule, ticket or chat.
