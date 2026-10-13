# Delivery proof

Author: Sayandip Bagchi.

---

## The hops and what proves each

```
MoEngage evaluates / flow trip
   │  proof: flow stats trip count; native alert "last triggered"
   ▼
Connector POST (flows)            ← no independent evidence; inferred from the next hop
   ▼
Intake logs a row                 ← A6a: AlertLog row, alertId, receipt stamp, uid/ref present
   ▼
Digest / relay                    ← evidence: the digest email or relay message
   ▼
Inbox                             ← A6b: Outlook message, subject, label, data window

Native alerts skip the intake: MoEngage email → inbox (A6b only).
```

Each hop can fail silently while the one before it looks healthy. Proof stops at the last hop with
evidence.

## A6a checklist

| Check | Pass |
|---|---|
| Row exists for `alertId` after go-live | row number quoted |
| Receipt stamp present | `ReceivedSerial` populated |
| `journey` equals the registry | exact |
| `uid` present | "present" |
| `ref` present iff the ref table says so | "present" / "blank by design" |
| No resolved values in the report | only presence stated |

A blank `ref` on an alert approved with one is escalated to `sentinel-flow` with the flow ID. A
present `ref` on a uid-only alert is a payload breach (security S5) and goes to the owner now.

## A6b checklist

| Check | Pass |
|---|---|
| Subject contains the alert name | exact |
| Workspace label | equals `config.json → workspaceEmailLabel` (not necessarily the header) |
| Data window | stated in the body; matches the expected evaluation |
| Recipient | a config recipient's inbox |
| Received time | recorded, with timezone |

## Common wrong conclusions

| Observation | Wrong conclusion | Right one |
|---|---|---|
| AlertLog has rows | "alerts are being delivered" | A6a only; A6b unproven until an inbox shows it |
| Email says another workspace's name | "the alert is in that workspace" | the label is the internal name; check the header workspace's list (Q13) |
| Email arrived hours after the set time | "schedule broken" | MoEngage evaluated on its schedule; match the window (Q15) |
| No email for a TEST alert after 10 min | "delivery broken" | wait for the next evaluation window before concluding |

## TEST alert record

| Field | Value |
|---|---|
| Name | `TEST <ID> <purpose> - <author> only (temp)` |
| Recipient | author only |
| Created | date, time, owner OK quote |
| First delivery | received time, window |
| Deleted | date, time, owner OK quote, list-view confirmation |
