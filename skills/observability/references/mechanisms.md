# Mechanisms: the four build types and their delivery paths

Author: Sayandip Bagchi.

What each build type is, how an alert travels from MoEngage to an inbox, and the platform
constraints that decide between them. The **decision rule** for a given sheet row is owned by
`alert-design` (`${CLAUDE_PLUGIN_ROOT}/skills/alert-design/references/design-rules.md`).

---

## Build types

| Build type | Where | Fires | Delivered by | Owning skill |
|---|---|---|---|---|
| `native_alert` | Settings → Reports and Alerts → Alert Management (Events Volume, Campaign Stats) | An aggregate threshold on event volume or campaign stats, evaluated on MoEngage's schedule over a data window | MoEngage email and, if enabled, MS Teams | `native-alert` |
| `system_alert_subscription` | Alert Management system alerts | A MoEngage-defined rule (for example Failure Rate Breach) | MoEngage email | `native-alert` |
| `sentinel_flow` | Flows (`/v4/create/flows`), a silent "MON" flow | Per qualifying user trip: a failure event, or an event with **no** follow-up inside a wait | Connector POST → Power Automate intake → intake log (AlertLog) → digest / relay → Outlook | `sentinel-flow` (MoEngage side), `alert-intake` (intake side) |
| `out_of_moengage` | none | none | A build ask to engineering or the analytics stack | `alert-design` records it |

## Delivery paths

```
native_alert ─────────────► MoEngage email ──────────────────────────────► Outlook
                            (and MS Teams)

sentinel_flow ─► Connector POST {alertId, journey, uid[, ref]}
                   ─► Power Automate intake (Parse JSON)
                       ─► AlertLog row (+ ReceivedSerial stamp)  ◄── A6a proves up to here
                           ─► digest / Teams relay ─► Outlook      ◄── A6b proves up to here
```

The two hops after MoEngage are separate proofs. An AlertLog row proves the intake received the
post; it says nothing about the digest or the inbox.

## The sentinel flow pattern

Entry: trigger event plus positive attribute filters (A2b). Optional condition: "has not done B
within W" (W ≥ 5 min). **YES → Exit. NO → Connector → Exit.** Only the NO branch posts. For a
failure-event flow there is no condition: trigger → Connector → Exit.

Fixed settings: control group off, audience All users, no customer-facing steps, frequency capping
off. The flow sends nothing to the customer.

**Sentinel flows have no threshold inside MoEngage.** Every qualifying trip posts. Counting,
windowing and paging happen at the intake or its digest. Never describe a flow as "fires above
N/day" unless the intake rule doing the counting is recorded in the tenant file.

## Constraints that drive the choice

| Constraint | Consequence |
|---|---|
| Flow wait minimum 5 min, maximum 30 days | A "within 3 minutes" stall cannot be a flow at 3 min; the owner approves 5 min or it goes elsewhere |
| No event-time token in the connector body | The intake stamps receipt time; latency analysis uses receipt time |
| Live flows cannot be edited or renamed | Every fix is a replacement with a new ID and a chain entry |
| Only trigger-event attributes are personalisable | `ref` must be an attribute of the trigger event; session-scoped IDs are unavailable |
| Native alerts evaluate on MoEngage's schedule over a data window | A native fire is matched by its data window, not the send minute |
| Events Volume cannot filter on arbitrary attributes | A per-attribute rule (a status value, a decline code) is a flow |

## Never both, silently

Do not build a native alert and a sentinel flow for the same signal unless the owner asks. When
both exist (a per-trip flow and a daily volume backstop, say), the registry `notes` on each row
says why.
