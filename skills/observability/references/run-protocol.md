# Run protocol

Author: Sayandip Bagchi.

The order of operations for every piece of live work. The step detail for each build type lives in
the owning skill; this file holds the sequence, the cross-cutting procedures (pause, polluted rows,
JS masking) and session hygiene. Gates are cited by number from [gates.md](gates.md).

---

## Build (any type)

1. **Model and mode gate** (router). Ask which model and plan vs direct; recommend Opus for builds.
2. Load the spec row from `tenants/<name>/alert-registry.csv`, or produce one with `alert-design`.
   Present it. **A0**: wait for approval of the alert, threshold or wait, recipients and payload.
3. **A1**: read the header workspace and env via JS. Stop on a mismatch.
4. **A2**: confirm events, attributes and values exist. **A2b**: filters are positive enumerations.
5. Build with the owning skill: `native-alert` or `sentinel-flow`.
6. **A3**: reopen and read back from the persisted state.
7. Publish. **A4**: list view shows Active.
8. **A5**: registry row and build log line, **now, for this object**. Long UI sessions lose context;
   a build log written at the end is a build log reconstructed from memory.
9. **A6a / A6b**: `delivery-verify`, separately. **A7**: `alert-health` shadow check within 24 h.
10. Report with [the change-report template](../templates/change-report.md).

## Replace (a live flow is wrong)

Live flows cannot be edited or renamed. Duplicate → rename (canvas click, breadcrumb check) → fix →
save → read back → publish → confirm Active → **pause the original** (below) → registry: new ID in
`moengage_id`, the old ID appended to the **full** `replaced_ids` chain with its reason. Suffix the
name `v2`, `v3`. Never delete a replaced original. Detail: `sentinel-flow`.

## Pause protocol

1. Open the flow and **wait for the page to finish loading**. Clicking Pause on a half-loaded page
   can act on nothing, or on a different control.
2. Click Pause and confirm **only if the "Pause the flow" dialog is present**. No dialog: stop,
   reload, retry once, then report.
3. Read the status **in the list view**, not the detail page. Paused versions do not show under the
   default Active filter; search the alert ID and use the **All** tab. The `paused` list filter
   value in the URL returns an error page.
4. Record the pause (ID, time, reason) in the registry chain and the tenant revisions.

## Polluted rows

When a flow is replaced because its **logic** was wrong (not its name or journey), every row it
wrote to the intake log is polluted, and every downstream count, digest and A7 ratio is wrong
until they go.

1. Identify the rows by `alertId` and the receipt window between the wrong flow's go-live and its
   pause. Count them.
2. Present the count and the window to the owner. **Delete only with the owner's OK** in session.
3. Delete, then re-read the log and confirm the remaining row count equals the expected figure
   (rows before minus rows deleted).
4. Record: alert ID, window, rows deleted, rows remaining, who approved, in the tenant revisions.

Rows written by a flow replaced for a cosmetic reason (name, journey label) are kept and annotated.

## JS output masking

The browser JS tool's output filter refuses to return strings that contain `=`, long hex runs or
query-like text, and those strings are also the ones most likely to hold a credential. Mask before
returning:

- slice the text from the "Body type" label downward (security S2);
- replace hex runs of 16+ characters with `<hex>`;
- replace `?` … `=` query fragments with `<query>`;
- return keys and token templates, not resolved values.

If the tool still refuses the output, return less, not more. Never widen the read to "see why".

## Verify delivery

`delivery-verify` owns it. A6a (intake row) and A6b (inbox) are separate proofs, never merged.

## Health

`alert-health` owns it. Read-only; every finding has an owner and a proposed action.

---

## Session hygiene

- **Before work:** ask plan mode vs direct and which model. Recommend Opus for builds.
- **Session length:** after 7–8 prompts of live UI work, offer a new session. Context loss shows up
  first as a wrong row clicked or a build log line reconstructed from memory.
- **Build log per object:** update the tenant build log / flow log after each flow, not at the end.
- **Re-screenshot before every coordinate click.** The screenshot frame and the CSS viewport can
  differ in size; coordinates from an older frame land on the wrong row. Prefer focusing a field
  via JS. If a wrong row was touched, discard the draft rather than patch it.
- **End:** write the context capsule ([template](../templates/context-capsule.md)) and ask whether the owner wants
  a YAML-frontmatter `.md` of new learnings for skill enhancement.
