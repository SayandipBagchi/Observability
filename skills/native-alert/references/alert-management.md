# Alert Management: fields, schedule, recipients

Author: Sayandip Bagchi.

Field-by-field build and read-back for native alerts. Values in angle brackets come from the
approved spec and the tenant config.

---

## Create

| Step | Field | Set to | Read-back check |
|---|---|---|---|
| 1 | Workspace header, env | `config.json → moengage.workspaceHeader`, `environment` | header text via JS equals config (A1) |
| 2 | Alert type | Events Volume / Campaign Stats | same after reopen |
| 3 | Event or campaign | `<event>` / `<campaign>` (+ channel) | exact name, not a similar one |
| 4 | Condition | `<, >, decreases by, increases by>` | operator unchanged |
| 5 | Threshold | `<n>` or `<n>%` | value unchanged |
| 6 | Comparison window | `in last Day` / `vs previous 7 days` | window unchanged |
| 7 | Schedule | the spec's cadence | stored cadence |
| 8 | Recipients | exactly `config.json → recipients` | list equals config, no extras |
| 9 | Channels | `config.json → nativeAlertChannels` | channels equal config |
| 10 | Name | `<Sev> <ID> <rule>` | exact string, no "(copy)" |

Save, close, reopen from the list, and read every row again. The spec-vs-read-back table goes in
the change report (A3).

## Split alerts

When one sheet row needs two native alerts (one per event, say), suffix the IDs `a`, `b`
(`XXX-04a`, `XXX-04b`), one registry row each, same `prd_ref`.

## Schedule and data window

- MoEngage evaluates on its schedule and states the data window in the email: "data considered …
  from X to Y". The send time can be minutes to hours after the window closes.
- Match a fire to its window (Q15). "Did it fire at the minute I set?" is the wrong question; "did the
  evaluation covering yesterday breach?" is the right one.
- A rule that compares with the previous 7 days needs 7 days of history before its first sensible
  evaluation; flag early fires after a new event starts.

## Recipients and subscribers

- The list view may show two named members and "+N others". Open the alert and list every
  subscriber before claiming the recipient set matches config.
- A subscriber not in config is reported to the owner with the alert name. Removing or adding one
  is a change that needs A0.

## Workspace switching

Workspace and env switches raise a confirmation and sometimes do not take in an automated tab
(Q14). After switching, read the header. Two failures → ask the owner to switch manually. Never
build "in the other workspace" on the strength of an email label (Q13).

## TEST alerts

TEST alerts are created only by `delivery-verify`, author-only, on a threshold certain to breach,
and deleted within 24 h of first delivery (Q16).
