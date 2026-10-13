# Alert description

Author: Sayandip Bagchi.

One plain-English paragraph per alert, for the PRD sheet or any stakeholder-facing table. It says
what broke, how the alert reaches people, what normal looks like, and the question it answers. No
event names in the first sentence; the logic column carries those.

## The four parts, in order

1. **What happened, in customer terms.** Start with the customer or the system, not the alert ID:
   "The customer started a payment but it was not confirmed within 20 minutes."
2. **How it pages.**
   - Sentinel flow: "Each case is logged to the intake with the user's MoEngage ID [and <ref name>],
     and an email goes out when there are N or more in X minutes or more than M in a day (H-hour
     cooldown)." Drop the path that is off (burst count 0 → "the daily email flags it when there
     are more than M in a day (no burst alert)"; daily threshold 0 → "there is no daily threshold").
   - Native alert: "MoEngage checks every morning at <time> and emails when <metric> for the
     previous day is <condition>."
   - System alert: name it, say it is MoEngage's own, give the threshold.
3. **Normal level.** The baseline with its window, from the **live** intake rules or the registry:
   "Normal level is about N a day (range a–b) (<window>)." If none was measured, say so plainly.
   If the logic changed since the baseline, say which logic the number belongs to and when it will
   be re-measured.
4. **The question it answers**, in quotes, plus at most one clause of context:
   It answers "is checkout failing?"

## Wording rules

- Daily thresholds: **"more than N in a day"** (the intake compares `> threshold`).
  Burst: **"N or more within X minutes"**.
- Numbers as the rule stores them; round baselines to what a reader needs (4.2, not 4.17).
- En dashes for ranges (2–11), no ID prefix when the sheet already has an ID column.
- Not built, paused or retired rows say so in the first two words ("Not built (paused).",
  "Retired.") and why.
- Never a resolved uid, ref value, recipient address or intake URL.

## Before writing to a sheet

Read the live rules first, then follow `${CLAUDE_PLUGIN_ROOT}/skills/alert-intake/references/sheet-sync.md`
(sheet-qualified addresses, per-batch read-back, no bulk undo). Record the written text in the
tenant folder.
