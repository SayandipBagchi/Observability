# Designer quirks

Author: Sayandip Bagchi.

Each quirk below has cost at least one rebuild. This file is the single numbered index; the full
procedure for a quirk lives in the skill that owns that surface, named in the last column. The
evidence (which alert, which day) is tenant state and lives in
`tenants/<name>/quirk-evidence.md`, keyed by the same number.

---

## MoEngage flows

| # | Quirk | Do this | Owner |
|---|---|---|---|
| Q1 | Create is at `/v4/create/flows`; duplicate is at `/v4/duplicate/flows/<id>`. | Use the URL; don't hunt through menus. | sentinel-flow |
| Q2 | **Live flows cannot be edited or renamed.** | Replace: duplicate → rename → set → save → read back → publish → pause original. | sentinel-flow |
| Q3 | A rename only sticks after editing the title **and** a real click on the canvas. | Check the breadcrumb shows the new name **before** Save, or "Duplicate - …" persists. | sentinel-flow |
| Q4 | The connector body editor keeps **one field change per save pass** when two fields are edited together. | Edit one key, blur, wait 2 s, edit the next, blur, save, reopen, read back all keys. | sentinel-flow |
| Q5 | "Keep evaluating" has a **minimum of 5 min** and a maximum of 30 days. | A spec under 5 min goes back to the owner for a 5-min approval. | alert-design |
| Q6 | Changing an event **clears its attribute rows**. | Set the event first, then attributes; re-check after any event change. | sentinel-flow |
| Q7 | The canvas **freezes when the Chrome tab is hidden**. | Keep the tab visible; reload if nodes stop responding. | sentinel-flow |
| Q8 | There is no event-time personalisation token for the connector body. | Don't send an event time; the intake stamps receipt time. | sentinel-flow |
| Q17 | The uid token is `{{UserAttribute['ID']}}`. What it resolves to is tenant-specific (a customer UUID or MoEngage's own 24-hex ID); record which in the tenant profile before anyone joins on it. | Confirm length and format from the first intake row (A6a). | sentinel-flow |
| Q18 | The ref token is `{{EventAttribute['MOE_TRIGGER_EVENT․<event>․<attr>']}}` and the separator is **U+2024 (one dot leader)**, not a full stop. Typing "." gives a token that saves, reads back plausibly and resolves to nothing. | Insert via the personalisation picker, or paste the U+2024 form; verify the code point in the JS read-back. | sentinel-flow |
| Q19 | Only the **trigger event's** attributes are personalisable. Session-scoped IDs are not in the picker. | Flows whose only identifier is session-scoped are uid-only by design; record the reason. | sentinel-flow |
| Q20 | The screenshot frame can differ in size from the CSS viewport. Coordinates from an older frame put a token in the wrong row. | Re-screenshot before every coordinate click, or focus the field via JS. If a wrong row was touched, discard the draft. | sentinel-flow |
| Q21 | Pause on a page that has not finished loading does nothing, or the wrong thing. | Wait for load; confirm only if the "Pause the flow" dialog appears; read status in the list view. | alert-retire |
| Q22 | The flows list URL `filter_block` accepts `active` and `all`; `paused` returns "Something went wrong". | To see paused versions, search the alert ID and click the **All** tab. | alert-retire |

## Attributes and filters

| # | Quirk | Do this | Owner |
|---|---|---|---|
| Q9 | A requirement sheet's "status" is usually a status attribute on the tenant's onboarding event, not a separate event. | Map it using the tenant's `vocabulary` in `config.json`. | alert-design |
| Q10 | OTP SMS are MoEngage **transactional alerts**, so SMS Sent/Delivered filter on `Alert Name`, not Campaign Name. | Filter by the exact alert name from the tenant config. | sentinel-flow |
| Q11 | Multi-select value pickers split labels with search highlighting. | Click "Clear all" first, then match the item by its full text. | sentinel-flow |
| Q12 | Sheet shorthand ("failed") rarely matches real enum values; payment-provider actions in particular use long snake-case values. | Pull real values from the event (A2); record the mapping in the registry. | alert-design |
| Q23 | Negative filters (`is not empty`, `!=`) pass values nobody considered, including success. | Positive enumeration only (gate A2b). | alert-design |

## Alert Management and email

| # | Quirk | Do this | Owner |
|---|---|---|---|
| Q13 | Alert emails show the workspace's **internal** name, which can differ from the header. | Verify objects in the header workspace's list view, never from the email label. | delivery-verify |
| Q14 | Workspace and environment switches raise a confirmation and sometimes don't take in an automated tab. | Read the header after switching; after two failed tries, ask the owner. | native-alert |
| Q15 | Native alerts evaluate on MoEngage's schedule, not the minute you set; the email states the data window. | Match a fire by its data window, not its send minute. | native-alert |
| Q16 | A TEST alert keeps firing until deleted. | Delete within 24 h of first delivery. | delivery-verify |

## Power Automate intake

| # | Quirk | Do this | Owner |
|---|---|---|---|
| Q24 | A Parse JSON schema edit doesn't commit until you click out and the panel re-renders; until then the dynamic picker won't offer the new fields. | Click out, reopen the action, read the schema back. | alert-intake |
| Q25 | When the picker lags, the expression `body('Parse_JSON')?['<key>']` works, but only if the expression popup is open; a click aimed at the editor with the popup closed lands on the canvas and opens another action. | Confirm the popup is open before typing. | alert-intake |
| Q26 | Mapping chips look right when the mapping is wrong. | Verify in **Code view** text; after Save, require the "Your flow is ready" banner. | alert-intake |

## Sheets, workbooks and docs

| # | Quirk | Do this | Owner |
|---|---|---|---|
| Q27 | **Excel Online Name box race:** typed text can land in the Name box or the Copilot pane instead of the cell, corrupting unrelated cells. | Click the target cell, zoom on the Name box to confirm the address, then type. Diff the saved copy against a baseline after every batch. | alert-intake |
| Q28 | The Excel saved copy (download) lags the UI by minutes, and it is the only valid verification. | Wait, re-download, verify there (gate A3). | alert-intake |
| Q29 | Tab inside an Excel table wraps to the next row. | Type headers and cells with direct clicks, never Tab. | alert-intake |
| Q30 | Google Sheets: Cmd+J focuses the Name box. | Navigate with it; verify via `/export?format=csv`. | alert-intake |
| Q31 | Google Docs on Mac: Cmd+End does nothing (use Cmd+Down); autocorrect turns "..." into "…" and capitalises after a full stop ("v2" → "V2"); a trailing italic style carries into new text. | Toggle italic off, check autocorrect damage, verify via Drive read-back. | alert-intake |
| Q33 | **Excel Online active sheet can change under you.** A tab click may not stick, or the workbook returns to another sheet between batches; a bare Name-box address (`C3`) then writes to whatever sheet is active. | Type **sheet-qualified** addresses in the Name box (`'<Sheet>'!C3`), screenshot the tab bar before each batch, and read back the first cell of every batch before continuing. | alert-intake |
| Q34 | **Bulk undo is not a restore.** Repeated Cmd+Z in Excel Online may not revert the batch you meant and can undo something else (Redo lights up with no visible change). | Never undo to recover. Restore each wrong cell from the baseline value, then read it back and record the address. | alert-intake |

## Browser tooling

| # | Quirk | Do this | Owner |
|---|---|---|---|
| Q32 | The Chrome JS tool's output filter blocks strings with `=`, long hex or query-like text. | Mask before returning (`run-protocol.md`, *JS output masking*). | observability |

## Security

| # | Quirk | Do this |
|---|---|---|
| S1 | The top of the connector drawer shows the intake URL **including its signature**. | Never screenshot the drawer; read the body via JS sliced from "Body type" (`security.md` S1, S2). |
| S2 | Once exposed, it is exposed. | Tell the owner the same turn; don't copy it; recommend rotation (`security.md` S3). |
| S3 | The Power Automate trigger card shows the same URL. | Never expand or screenshot it (`security.md` S1). |
| S4 | A JS read of the whole drawer returns URL parameters. | Slice from "Body type"; no screenshot while any drawer is open (`security.md` S2). |

New quirks get the next free number, a row here, the procedure in the owning skill, and the
evidence in the tenant's `quirk-evidence.md`.

## Watchdog and Power Automate expression quirks (Q35–Q45)

Q35 read-after-write lag in the intake's burst count, Q36 integer division, Q37 float literals, Q38 `createArray()` with no arguments, Q39 Excel pagination, Q40 string values and blanks, Q41 typed `@` expressions and the fx editor, Q42 parallel loops, Q43 the platform's weekly failure summary, Q44 Excel Online ignoring synthetic input, Q45 resubmit is not proof. Full table: `${CLAUDE_PLUGIN_ROOT}/skills/alert-watchdog/references/watchdog-quirks.md`.
