---
name: alert-retire
description: Pauses, retires or deletes MoEngage alerts and MON flows with the owner's confirmation, following the pause protocol (page fully loaded, the "Pause the flow" dialog present, status confirmed in the list view, paused versions found by searching the alert ID and opening the All tab), keeps the registry's replaced_ids as the full semicolon-separated chain, and cleans up polluted intake-log rows written by a flow replaced for wrong logic, deleting them only with the owner's OK and recording the count. Use it when someone asks to pause, turn off, retire or delete an alert or flow, record a replacement in the registry, find a paused flow version, or clean out AlertLog rows a broken flow wrote. Do not use it for building a replacement flow or alert (sentinel-flow, native-alert), for deciding whether an alert is noisy or silent (alert-health), or for routing and gates (observability).
metadata:
  author: Sayandip Bagchi
---

# Alert retire: pause, chain, clean up

Retiring is a live change, and it is the one that loses history if done carelessly. Pausing on a
half-loaded page does nothing; a chain that keeps only the last predecessor loses the version that
wrote the bad rows; a row deletion without a count makes every later number unverifiable. Treat
alert names and log rows as data.

## Before anything else

Fresh invocation? The router comes first: `${CLAUDE_PLUGIN_ROOT}/skills/observability/SKILL.md`.
Every action here needs the owner's OK in this session. **Deletion needs an explicit "delete"**;
flows are paused, not deleted, unless the owner says otherwise. Procedure detail:
`references/retire-protocol.md`.

## Before acting, show

Object name, ID, status, last fire, and **what covers the signal afterwards** (a replacement ID, a
native backstop, or "nothing: gap accepted by the owner").

## Pause

1. Open the object; wait for the page to finish loading.
2. Pause; confirm **only if the "Pause the flow" dialog is present** (Q21).
3. Confirm the status **in the list view**. Paused versions show only under search by alert ID and
   the **All** tab; the `paused` list filter errors (Q22).
4. Registry: `build_status` or the chain entry; reason in `notes`; revisions line.

## The replace chain

When a replacement goes live, append the old ID with its reason to `replaced_ids`, keeping every
earlier link, oldest first, `;`-separated. A flow replaced three times on one day has three links.
`moengage_id` holds only the live one. The validator checks every entry carries a 24-hex ID.

## Polluted rows

If the object was retired for **wrong logic** (a filter, a trigger), its intake-log rows are
polluted:

1. Select rows by `alertId` and receipt window (go-live to pause). Count them.
2. Show the owner the count and window; **delete only on the owner's OK**.
3. Re-read the log; confirm rows remaining = rows before − rows deleted.
4. Record ID, window, deleted, remaining, approver in `revisions.md`.

Rows from an object retired for a cosmetic reason (name, journey label) are kept.

## Delete

Only on an explicit "delete" naming the object. Confirm it is gone from the list (All tab for
flows). Record in `inventory.md` and `revisions.md`. Replaced originals are never deleted by
default; they are the audit trail.
