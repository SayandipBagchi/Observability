# Health checks

Author: Sayandip Bagchi.

---

## Registry vs live: the matching rules

| Build type | Match on | Live evidence |
|---|---|---|
| `sentinel_flow` | `moengage_id` (24-hex) | Flows list row, status Active |
| `native_alert` | exact `moengage_name` (IDs are shown on the alert page) | Alert Management list row |
| `system_alert_subscription` | system alert name | subscriber list includes config recipients |
| `out_of_moengage`, `not_built` | nothing live expected | a live object with that ID is an orphan finding |

Finding vocabulary: `MISSING` (registry live, not in list) · `PAUSED` (registry live, list paused) ·
`NAME_DRIFT` · `ID_DRIFT` · `ORPHAN` · `PREDECESSOR_ACTIVE` · `SILENT` · `EXPECTED_SILENCE` ·
`NOISY` · `STALE_VERIFY` · `SUSPECT_LOGIC` · `SUBSCRIBER_DRIFT` · `NOT CHECKED`.

## Reading the lists

- Read list text via JS. Do not open connector drawers during a health check; there is nothing in
  them this check needs.
- The Flows list defaults to Active. To see paused predecessors, search the alert ID and click
  **All**. The `paused` value of the list's `filter_block` URL parameter returns an error page (Q22).
- Alert Management may show "+N others" for subscribers; open the alert to list them (subscriber
  drift is checked against `config.json → recipients`).

## The shadow check (A7) in numbers

```
window    = [go_live, go_live + 24h)
fires     = count(AlertLog rows where alertId = <ID> and receipt in window
                  and the row is not attributable to a paused predecessor)
baseline  = registry baseline, events per day
ratio     = fires / baseline
verdict   = SUSPECT_LOGIC if ratio > 3 (settings.json → health.shadowCheck.suspectMultiple)
            SILENT        if fires = 0 and baseline > 0 and not acquisition-dependent-while-paused
            PASS          otherwise
```

Report: ID, flow ID, window start and end with timezone, fires, baseline, ratio, verdict, the
trigger filter list, and whether any filter is negative.

### Why over 3× is logic, not incident

A 24-hour window after go-live is a replay of normal traffic through new logic. A genuine incident
can coincide with go-live, but the base rate strongly favours a filter that admits too much. The
cheap test is the filter list: a negative operator, a missing enumeration, or a trigger event that
also fires on success. If the filters are clean positive enumerations, say so and escalate to the
owner as a possible real spike, with the evidence.

## Acquisition-dependent silence

When `config.json → acquisitionPaused.value` is true, rows with `acquisition_dependent` = yes (any
variant) are expected to be quiet. Report them as `EXPECTED_SILENCE` with the pause date, never as
broken, and never propose deleting or loosening them. Expected silence is still checked:

1. **Confirm the flow is still Active** in the list view (search the alert ID; use the All tab to
   see paused versions). A paused or missing flow is `PAUSED` / `MISSING`, not expected silence.
2. **Record when the trigger event was last seen** (date of its last occurrence), so a trigger that
   died for another reason is not hidden behind the acquisition pause.
3. **Schedule a re-check once acquisition resumes**: add an open item with the owner, to confirm
   the alert fires within its baseline and to re-run the A7 shadow check.
4. The baseline convention for a stopped event (window ending on the last day it fired, labelled)
   is in `${CLAUDE_PLUGIN_ROOT}/skills/alert-design/references/baselines-and-fire-rate.md`.

## Report format

```
<date> · <tenant> · <workspace> (<env>) · registry <n> rows · validator OK/errors
ID · finding · evidence · owner · proposed action
...
Counts: live flows n, live native n, subscriptions n, paused n, not built n, NOT CHECKED n
```
