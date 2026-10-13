# Flow build and replace, step by step

Author: Sayandip Bagchi.

Quirk numbers refer to `${CLAUDE_PLUGIN_ROOT}/skills/observability/references/designer-quirks.md`.

---

## New flow

| # | Step | Check before moving on |
|---|---|---|
| 1 | A1: read header workspace and env via JS | equals `config.json` |
| 2 | A2: the trigger event, follow-up event, filter attribute and each enumerated value exist | value counts from a recent occurrence |
| 3 | Open `/v4/create/flows` (Q1) | blank canvas, tab visible (Q7) |
| 4 | Trigger: set the **event first**, then attribute rows (Q6) | attributes still present after any event change |
| 5 | Filters: `in [<approved values>]`, picker cleared first (Q11), matched by full text | no `is not empty`, `!=`, `not in` (A2b) |
| 6 | Condition (stalls only): "has not done `<follow-up>` within W" | W ≥ 5 min (Q5) |
| 7 | YES → Exit. NO → Connector | only the NO branch reaches the connector |
| 8 | Connector: POST, JSON. Keys one per save pass (Q4) | see *Connector body* below |
| 9 | Settings: control group off, audience All users, frequency capping off, no customer step | |
| 10 | Name `MON <ID> <rule>`; click the canvas; breadcrumb shows the name (Q3) | before Save |
| 11 | Save; **close and reopen** | the toast is not evidence |
| 12 | A3 read-back (below) | every field equals the spec |
| 13 | Publish; A4: list view shows Active | list row text |
| 14 | A5: registry row and build log line now | diff printed |

## Connector body

Target body:

```json
{"alertId": "XXX-01", "journey": "<journey>", "uid": "{{UserAttribute['ID']}}", "ref": "{{EventAttribute['MOE_TRIGGER_EVENT․<event>․<attribute>']}}"}
```

Omit `ref` for a uid-only flow; never send an empty `ref` key. Enter keys one per pass: set
`alertId`, blur, wait 2 s, save; set `journey`, blur, save; and so on, reopening between passes
if a key has previously been lost. Insert the `ref` token through the personalisation picker where
possible; if pasted, paste the U+2024 form (`payload-tokens.md`).

## Read-back (A3)

| Field | How | Pass when |
|---|---|---|
| Name | breadcrumb and list row | exact string, no "Duplicate - " prefix |
| Trigger event and filters | canvas node | event, operator `in`, values equal the approved list |
| Wait | condition node | equals spec |
| Connector keys | JS, sliced from "Body type" down, masked | keys exactly `alertId`, `journey`, `uid`[, `ref`] |
| `alertId`, `journey` | same JS read | equal spec (a copied flow often keeps its parent's values) |
| Tokens | same JS read | uid template exact; ref separator is U+2024 (check the code point, not the glyph) |

## Replace a live flow

Any change to a live flow, including a rename, is a replacement (Q2).

1. `/v4/duplicate/flows/<live id>`.
2. Rename, then a real canvas click, then check the breadcrumb (Q3). Suffix `v2`, `v3`.
3. Fix the one thing that was wrong. Re-check `alertId` and `journey`: duplicates carry the parent's.
4. Save, reopen, full A3 read-back.
5. Publish; A4.
6. Pause the original using the pause protocol (router `run-protocol.md`): page fully loaded,
   "Pause the flow" dialog present, status read in the list view. Paused versions appear only under
   search + **All** (Q22).
7. Registry: `moengage_id` = new ID; append the old ID with its reason to `replaced_ids`, keeping
   every earlier link, `;`-separated.
8. If the original was wrong in its **logic** (filters, trigger), its intake rows are polluted:
   hand the cleanup to `alert-retire` with the go-live and pause times.
9. Build log line now.

## When the ask is to fix a filter

A wrong filter is the most expensive defect here because the flow has already posted. Replace, then
A7 on the replacement, then polluted-row cleanup for the original. Tell the owner the count of rows
the wrong version wrote before anything is deleted.
