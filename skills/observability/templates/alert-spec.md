# Alert spec: <ID>

Produced by `alert-design`. Presented to the owner for A0; nothing is built from an unapproved
spec. One spec per alert ID.

| Field | Value |
|---|---|
| Alert ID / PRD ref | `XXX-01` / sheet row |
| Module · KPI | |
| Severity | P1 / P2 / P3 |
| Build type | native_alert / sentinel_flow / system_alert_subscription / out_of_moengage |
| Why this build type | aggregate threshold → native; per-user break or every-failure → flow |
| Trigger event | `<trigger event>` |
| Attribute filters (positive enumeration only, A2b) | `<attribute> in [<value 1>, <value 2>]` |
| Exclusions (only if approved, narrowing a positive anchor) | none / `<attribute> != <value>` with reason |
| Condition / wait (flows) | "has not done `<follow-up event>` within W" (W ≥ 5 min) or every event |
| Threshold / window (native) | e.g. `< 2 in last Day`, `decreases > 40% vs previous 7 days` |
| Schedule / data window (native) | |
| Baseline | `<n>/d (<min>–<max>) · <from>–<to>`, 30-day average to the last day the event fired |
| Expected fires per week at this threshold | from `baselines-and-fire-rate.md` |
| Journey (flows) | one of the tenant's journey values |
| Payload (flows) | `alertId`, `journey`, `uid`, `ref` = `MOE_TRIGGER_EVENT.<event>.<attr>` (stored form) or "uid only" + reason |
| Name | `<Sev> <ID> <rule>` (native) or `MON <ID> <rule>` (flow) |
| Recipients | from tenant `config.json` only |
| Acquisition-dependent? | yes / yes (proposed) / no |
| Open questions | |

**Approval (A0):** ☐ alert ☐ threshold/wait ☐ recipients ☐ payload — owner, date, time, in-session quote.
