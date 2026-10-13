# Retire protocol

Author: Sayandip Bagchi.

---

## Decision table

| Situation | Action | Owner words needed | Registry |
|---|---|---|---|
| Flow replaced by a new version | pause original | "ok pause" (or the replacement approval covering it) | chain entry `<id> (PAUSED, <reason>)` |
| Alert no longer wanted, signal covered elsewhere | pause | "ok pause" | `build_status = paused`, note names the cover |
| Alert no longer wanted, no cover | pause | "ok pause, gap accepted" | note records the accepted gap |
| Process stopped (source event dead) | pause or leave; propose | decision | `acquisition_dependent` / note |
| Native alert superseded by a flow | delete native (if owner says delete) | explicit "delete" | `build_status = retired`, note names the flow |
| TEST alert after delivery | delete | "ok delete" | inventory + revisions only |

## Pause, precisely

1. Navigate to the flow by ID. Wait for the canvas and header to load fully (no spinners).
2. Click Pause. A "Pause the flow" confirmation dialog must appear. If it does not, do not click
   anything else on the page: reload, wait, retry once, then stop and report.
3. Confirm in the dialog.
4. Go to the Flows list, search the alert ID, open **All**, and read the row's status. "Paused" in
   the list is the evidence; the detail page's button state is not.
5. Record time and evidence.

## Finding paused versions

- The Flows list's `filter_block` accepts `active` and `all`; `paused` returns "Something went
  wrong" (Q22).
- Search the alert ID, then click the **All** tab. Every version, including `Duplicate - …` names
  and `v2`/`v3` suffixes, appears there.

## Chain format

```
replaced_ids = "<v1 id> (PAUSED, <reason>);<v2 id> (PAUSED, <reason>)"
moengage_id  = "<v3 id>"
```

Oldest first. Never rewrite an earlier link's reason; append.

## Polluted-row cleanup record

| Field | Example shape |
|---|---|
| Alert ID and flow ID | `XXX-01`, `<24-hex>` |
| Reason polluted | "negative filter admitted successes" |
| Window | go-live → pause, with timezone |
| Rows before / deleted / remaining | n / d / n − d |
| Verified remaining by | re-read of the log, time |
| Approved by | owner, quote, time |

The cleanup is recorded in the tenant `revisions.md` and referenced in the replacement's registry
`notes`.
