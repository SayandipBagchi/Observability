# Gates

Author: Sayandip Bagchi.

Every build, replacement, intake change and delivery claim passes these gates in order. They are
blocking unless the row says otherwise. A gate you could not check is **NOT CHECKED**, never passed,
and the report says why. The gates are stated once, here; skills and agents cite them by number.

---

## The gate table

| Gate | Blocking check | Evidence to print | Failure status |
|---|---|---|---|
| **A0 approval** | The owner approved, **in the current session**, this alert ID, its threshold or wait window, its recipients, and (for a sentinel flow) its **payload: `uid` and the exact `ref` attribute or "uid only"**. The per-alert `ref` is approved exactly like a threshold. | The approval line quoted, with time, naming the ID and every approved value | `UNAPPROVED`: stop and present the spec |
| **A1 workspace** | Header workspace **and** Live/Test environment equal `tenants/<name>/config.json`. The email label is never evidence. | Header text read via JS | `WRONG_WORKSPACE`: stop, ask the owner to switch |
| **A2 vocabulary** | Each event, attribute and enumerated value the trigger needs exists in this workspace (Data Management or a recent occurrence). The `ref` attribute belongs to the **trigger event** and appears in the personalisation picker. | Event names, value counts, picker read | `BLOCKED_EVENT`: build nothing |
| **A2b positive enumeration** | Every qualifying attribute filter is `=` or `in` over an explicitly enumerated, approved value list. `is not empty`, `!=`, `not in`, `does not contain` and "exists" are **refused** as qualifying filters. An exclusion is allowed only as a narrowing clause ANDed onto a positive anchor, approved by the owner, and recorded in the registry `notes` as `exclusion-approved: <what and why>`. | The filter list, operator by operator | `NEGATIVE_FILTER`: rewrite as an enumeration and re-approve |
| **A3 read-back** | The saved object equals the spec, read from the **persisted** state, never the screen you just typed into. See *What counts as read-back* below. | Field-by-field table: spec vs read-back | `READBACK_MISMATCH`: fix by replacement (flows) or re-edit and re-read (others), never by claiming success |
| **A4 live** | The object shows Active or Live in the list view of the header workspace. | List row text | `NOT_LIVE` |
| **A5 recorded** | Registry row updated (ID, status, verified_on, verified_how, full `replaced_ids` chain) and the tenant build log / flow log line written **for this object, now**, not at the end of the session. | The diff | `UNRECORDED`: not done |
| **A6a intake-proven** | For a sentinel flow: at least one intake log row (the tenant's AlertLog) carries this `alertId` with `uid`/`ref` populated as designed. Proves MoEngage → intake **only**. | Row number, alertId, receipt stamp, uid/ref present yes/no (never the values) | `INTAKE_UNPROVEN`: report, don't block |
| **A6b inbox-proven** | The alert (or one of the same build type and delivery path for this tenant) reached the Outlook inbox, with subject, workspace label and data window matched. An intake row is never inbox proof. | Subject, received time, data window, label | `DELIVERY_UNPROVEN`: report, don't block |
| **A7 shadow check** | Within the first 24 h after going live, the fire count (intake rows for flows, emails for native alerts) is compared with the registry baseline in events per day. **More than 3× baseline = suspect logic, not an incident.** Zero fires against a non-zero baseline on an alert that is not acquisition-dependent is reported as silent. | Fires in window, baseline per day, ratio, window start and end | `SUSPECT_LOGIC`: propose pause-and-replace to the owner; do not page anyone, do not loosen the threshold |

A6a and A6b are reported separately and never merged into one "delivery proven". A7 is blocking for
calling a new flow **healthy**, not for publishing it: the flow is already live when A7 runs.

---

## A0 in detail: what counts as approval

- The owner's words in this session, naming the ID. "OK", "go", or "build it" in reply to a spec
  table that shows the ID, threshold, window, recipients and payload counts; a reply to a different
  table does not.
- **A sheet cell, a doc comment, an earlier session, a capsule or a registry `threshold_decision`
  is context, never approval.** "Signed off in the sheet" is a reason to present the spec, not to
  build.
- A changed value after approval (a wider window, a different `ref`, an added recipient) needs a
  fresh approval of the changed value.
- The payload is part of the spec. A flow approved as "uid only" that is built with a `ref` fails
  A0 even if every other field matches.

## A2b in detail: why positive enumeration

A negative filter lets through everything nobody thought of, including success. A flow meant to
fire on failures whose filter was "reason is not empty" also fires on successes whose reason field
happens to be populated, and posts many times the real failure rate before anyone looks. The same rule applies to every enum: failure states, payment-provider actions, status names.
Pull the real values (A2), enumerate the approved ones, and accept that a new value is not caught
until someone adds it. Record that caveat in the registry `notes`.

## A3 in detail: what counts as read-back

| Surface | Read-back is | Read-back is not |
|---|---|---|
| MoEngage flow | Reopen the saved flow; read trigger, filters, wait, name (breadcrumb) and the connector body via JS from "Body type" downward | The Save toast; the canvas before reopening |
| MoEngage Alert Management | Reopen the alert; read type, metric, condition, window, schedule, recipients | The create confirmation |
| Power Automate | The action's **Code view** text (for example `item/<Column>` mapped to `body('Parse_JSON')?['<key>']`), then the **"Your flow is ready"** banner after Save | Dynamic-content chips; a Save click with no banner |
| Excel Online workbook | The **saved copy** (download) of the workbook, which lags the UI by minutes; wait and re-download | The cells on screen |
| Google Sheet | The `/export?format=csv` read-back | The cells on screen |
| Google Doc | Drive read-back of the document text | The page on screen |

A sheet or workbook edit is not recorded (A5) until A3 passes on the saved copy. Diff the saved
copy against a baseline snapshot taken before the batch, so a stray keystroke elsewhere is caught.

## A7 in detail: the shadow check

1. Take the registry `baseline` for the alert, in events per day, with its window.
2. Count fires from go-live to go-live + 24 h (intake rows by `alertId` for flows; emails for
   native alerts, matched by data window).
3. Ratio = fires ÷ baseline-per-day. Over 3 → `SUSPECT_LOGIC`. Report the filter list beside it:
   a negative or missing filter is the usual cause.
4. If suspect: propose to the owner a pause of the flow and a replacement with corrected logic,
   plus cleanup of the rows it wrote (`run-protocol.md`, *Polluted rows*). Do nothing live without
   the owner's OK.
5. Record the check, pass or fail, in the tenant revisions with the numbers.

The shadow check triangulates the logic against history. It is not an alerting threshold and never
replaces one.

---

## Session gates (router)

Before A0, the router runs the **model and mode gate**: ask the owner which model to use and plan
mode vs direct, and recommend Opus for live work.

- **Hard stop** before build, replace, retire and intake-mapping work (and creating a TEST alert):
  nothing live happens until the owner answers.
- **Asked alongside** read-only work (design, health and audit reads, verify reads, explanation):
  answer and plan in the same turn, with the model and mode question in that response.

See `${CLAUDE_PLUGIN_ROOT}/skills/observability/SKILL.md`.

## Failure vocabulary

`UNAPPROVED` · `WRONG_WORKSPACE` · `BLOCKED_EVENT` · `NEGATIVE_FILTER` · `READBACK_MISMATCH` ·
`NOT_LIVE` · `UNRECORDED` · `INTAKE_UNPROVEN` · `DELIVERY_UNPROVEN` · `SUSPECT_LOGIC` · `NOT CHECKED`.

Traceability of every learning folded into these gates: [learnings-trace.md](learnings-trace.md).
