# Sheet, workbook and doc sync

Author: Sayandip Bagchi.

The alerting records (PRD tables, status columns, flow logs, handoff docs) live in Excel Online,
Google Sheets and Google Docs. Each has a way of showing you text that was never saved, or saving
text you never meant to type. Verification is always against the persisted copy (gate A3).

---

## Before any batch

1. Take a **baseline snapshot** of the persisted state: download the workbook, export the sheet as
   CSV, or read the doc through Drive.
2. List the cells or lines to change, with their current values.
3. After the batch, take the same snapshot again and **diff**. Every changed cell must be on the
   list; anything else is corruption to report and restore.

## Excel Online

| Quirk | Procedure |
|---|---|
| **Name box race** (Q27) | Click the target cell. Zoom on the Name box and confirm it shows that address. Only then type. After a batch, diff against the baseline: typed text that went into the Name box navigates or renames; text that went into the Copilot pane is lost; both can leave unrelated cells edited. |
| **Saved copy lags** (Q28) | The downloaded workbook can be minutes behind the screen. Wait, re-download, verify there. The screen is never evidence. |
| **Tab wraps** (Q29) | Inside a table, Tab at the last column moves to the next row. Type headers and cells with direct clicks. |
| **Active sheet changes** (Q33) | Write with sheet-qualified Name-box addresses (`'<Sheet>'!C3`), never bare ones, when the workbook has more than one tab. Screenshot the tab bar before each batch and read back the first cell of the batch before writing the rest. |
| **Bulk undo** (Q34) | Never use Cmd+Z repeatedly to reverse a wrong batch. It may not revert it and may undo something else. |
| Restoring | Restore from the baseline value, cell by cell, then verify in a fresh saved copy. Record every restored address. If the prior value of a cell was never captured, say so and mark it for a Version History check rather than guessing silently. |

## Description cells

When a PRD or registry sheet gets per-alert description text, write it in the format of
`${CLAUDE_PLUGIN_ROOT}/skills/observability/templates/alert-description.md`, take thresholds and
baselines from the **live** intake rules (not a saved snapshot), and record the written text in the
tenant folder so the next session can diff the sheet against it.

## Google Sheets

- Cmd+J focuses the Name box (Q30): type the address, Enter, then type the value.
- Verify through `/export?format=csv` for the tab, compared with the baseline export.

## Google Docs

- On Mac, Cmd+End does nothing; Cmd+Down goes to the end (Q31).
- Autocorrect turns "..." into "…" and capitalises after a full stop ("v2" → "V2"). Re-read IDs and
  version labels after typing.
- A trailing italic style carries into new text; toggle it off before typing.
- Verify through a Drive read-back of the document text.

## What gets reported

Per surface: cells or lines changed, the baseline and after snapshots used, every unexpected diff
with its address and restore evidence, and anything still lagging ("saved copy not yet showing
<cell>; re-check at <time>"). A batch is not recorded (A5) until its saved copy verifies.
