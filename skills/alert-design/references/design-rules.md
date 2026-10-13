# Design rules

Author: Sayandip Bagchi.

The detail behind the decision rule in `../SKILL.md`, the shapes each build type takes, and how a
sheet row becomes a spec. Placeholders only; the tenant's real alerts are in its registry and
`journeys.md`.

---

## Signal shapes and their build type

| Signal shape | Build type | Spec shape |
|---|---|---|
| Daily or 7-day volume of one event, up or down | `native_alert`, Events Volume | `<event> decreases by > 40% vs previous 7 days` |
| Campaign metric (sent, failure, bounce) per campaign or channel | `native_alert`, Campaign Stats | `<campaign> Sent < 2 in last Day` |
| MoEngage already ships the rule | `system_alert_subscription` | subscribe; record the system threshold |
| A failure event where every occurrence matters | `sentinel_flow`, every event | `<event> <status attribute> in [failure]` → Connector |
| A step that did not follow another within a window | `sentinel_flow`, stall | `<event A>` → NO `<event B>` within W → Connector |
| An enumerated set of failure values on one event | `sentinel_flow`, every event | `<event> <code attribute> in [<code 1>, …, <code n>]` |
| The data is not in MoEngage | `out_of_moengage` | build ask with owner |

### Why aggregate goes native and per-user goes to a flow

- Native alerts evaluate a **count or rate over a data window** on MoEngage's schedule and email
  directly. They cannot say who. They are cheap and need no intake.
- A sentinel flow evaluates **each user's trip**. It can say who (uid) and which case (ref), and
  it catches a single broken journey the day's aggregate hides. It has no threshold inside
  MoEngage: every qualifying trip posts, and counting happens at the intake.
- So: "is the rate bad today?" → native. "Did this customer get stuck?" or "did this failure
  happen?" → flow.

## From sheet row to spec

1. Copy ID, module, KPI, severity verbatim. Keep the sheet's wording in `threshold_decision`.
2. Map each named event to a real event in the tenant vocabulary. A sheet "status" is usually a
   status attribute on the tenant's onboarding event (quirk Q9). Pull the real values; shorthand
   such as "failed" rarely matches (Q12).
3. Choose the build type with the decision rule; write the row that matched.
4. Write filters as positive enumerations (A2b). An `is not empty` or `!=` in the sheet is
   rewritten as the enumerated approved values, with the list shown to the owner. **Caveat:** a
   new enumerated value (a new decline code, status or payment-provider action) is not caught until it is added
   to the list and approved, and the flow is replaced. Record that caveat in the registry `notes`
   for the alert; the note is required.
5. For a stall, set W from the product's expectation, floored at 5 min (Q5).
6. Baseline and fire rate per `baselines-and-fire-rate.md`.
7. Propose the payload: `uid`, and `ref` only if the trigger event carries a case identifier.
   Check the tenant's `ref-table.md`; a ref not in the table is a new approval.
8. Name: `<Sev> <ID> <rule>` for native, `MON <ID> <rule>` for flows, plain language, no symbols
   the UI mangles.
9. Flag acquisition dependence.

## The approval table is the deliverable

A spec with no approval table is not finished. The owner approves per ID and per value: alert,
threshold or wait, payload. A partial approval ("XXX-03 yes but 10 min not 5") produces a revised
spec row, shown again.

## Payload approval (A0)

The per-alert `ref` is approved like a threshold because it decides which customer data leaves
MoEngage. Present it as the stored form `MOE_TRIGGER_EVENT.<event>.<attribute>` and say what it
identifies (a transaction, an application, a mandate). "uid only" is a decision too and carries a
reason: no case identifier on the trigger event, or the identifier is session-scoped.

## Things that go back to the owner

- Wait under 5 min · threshold that would fire daily · threshold that could never fire · a
  percentage on a tiny base · a negative filter · a ref outside the ref table · a second build for a
  signal already covered · a signal outside MoEngage.
