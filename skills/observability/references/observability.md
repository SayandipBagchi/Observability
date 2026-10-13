# Observability: watching the alerts, and watching the alerting

Author: Sayandip Bagchi.

An alert that never fires looks exactly like a healthy business. The gates prove a build at the
moment it went live; this file is the standing discipline that notices when the alerting itself
stops working. Two layers: the **alerts** (are they firing as designed?) and the **agent** (did the
session that built them leave a trace someone else can check?).

---

## Layer 1 · Observing the alerts

### Signals per build type

| Build type | Fire evidence | Where to read it |
|---|---|---|
| `native_alert` | Email with subject = alert name, data window stated | Outlook search by alert name |
| `sentinel_flow` | Intake log row with `alertId`; flow trip count | Intake log (AlertLog); flow stats |
| `system_alert_subscription` | Email from the system alert | Outlook |

### Triangulation pairs

| Pair | Should agree because | A gap means |
|---|---|---|
| Intake log rows vs flow trips reaching the connector | Every NO-branch trip posts once | Posts failing at the intake, or a flow posting from a paused version |
| First-24h fires vs registry baseline (A7) | The baseline is the same rule over history | > 3× suspect logic; 0 against a non-zero baseline = silent |
| Native email data window vs the schedule | MoEngage evaluates on its own schedule | Match by window; a missing window is a missed evaluation |
| `uid` / `ref` in the intake log vs the tenant's customer data | uid is the customer key; ref is the trigger event's ID | Wrong token (Q17/Q18) or wrong attribute |
| Intake log (A6a) vs inbox (A6b) | Digest / relay forwards what the log holds | A broken digest or relay; never inferred from the log |

### Silent and noisy thresholds

`settings.json → health` holds the defaults: `silentAlertDays`, `noisyAlertFiresPerWeek`,
`maxHoursSinceRegistryVerify`, and `shadowCheck.suspectMultiple` (3). A silent alert on an
acquisition-dependent row while acquisition is paused is **expected**, and says so, rather than
being reported as broken.

### Drift

| Kind | Detector |
|---|---|
| Vocabulary drift | A trigger value or event stops appearing (A2 on re-check); a new enum value appears that the positive enumeration does not include |
| Registry-vs-live drift | `alert-health`: registry says live, list says paused or missing; name mismatch; orphans (`MON`, `P1`–`P3`, `TEST` objects not in the registry) |
| Doc-vs-live drift | Sheet or workbook status column disagrees with the registry |

## Layer 2 · Observing the agent

- **Build trace:** one change-report line per object, written as the object is built, carrying the
  approval quote, the gate evidence, and the ID.
- **Build log:** the tenant's build log CSV updated per flow (`run-protocol.md`).
- **Failure taxonomy:** the gate failure statuses in `gates.md`. Every failure in a report uses one.
- **Security trace:** the change report's Security line is never blank: "no exposure" or the
  exposure and the owner's decision.

Every observation becomes one of: a registry note, an open item with an owner, or a question to the
owner. Never nothing.
