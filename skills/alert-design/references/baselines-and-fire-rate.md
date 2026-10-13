# Baselines and fire-rate estimates

Author: Sayandip Bagchi.

A threshold is only as good as the history it was set against. This file says how to state that
history and how to turn it into an expected fire rate, which becomes the yardstick for the A7
shadow check after go-live.

---

## The baseline convention

- **30-day average ending on the last day the event fired**, with daily min–max and the window:
  `12.0/d (4–25) · <from>–<to>`.
- If the event stopped (a process paused, an integration switched off), end the window at the last
  fire and say so: `… · last seen <date>`. A baseline that ends before today is still a baseline,
  labelled.
- If the event started recently, use the full available history and say how many days.
- For a stall (A → NO B within W), baseline the **not-progressed count per day**, not A's volume:
  A/day × (1 − share reaching B within W).
- For a rate, give numerator and denominator per day as well as the rate. A rate on a base under
  about 5/day swings on single events.

## Estimating fires per week

Use the **daily series**, never the average alone.

| Build type | Fires per week ≈ |
|---|---|
| Native, threshold on a daily count | number of days in the last 30 on which the rule would have been true × 7/30 |
| Native, % change vs previous 7 days | days on which the change would have exceeded the threshold × 7/30 |
| Flow, every event | baseline/day × 7 (each event posts) |
| Flow, stall | not-progressed/day × 7 |

Flow numbers are **posts**, not emails: the intake or digest decides what reaches an inbox. Say so.

## Red flags to raise before approval

| Flag | Test | Say |
|---|---|---|
| Noise | rule true on more than ~1 day in 3 of the baseline | "would fire most days; propose <alternative>" |
| Silence | rule true on 0 days and the gap to threshold is large | "would never have fired; is that the intent?" |
| Tiny base | rate threshold with base < ~5/day | "use an absolute count instead" |
| Stopped source | last seen well before today | "will be silent until the process resumes" |
| Acquisition | trigger only happens for new applicants | "silent while acquisition is paused" |

## After go-live: the same numbers, reversed

The A7 shadow check (`${CLAUDE_PLUGIN_ROOT}/skills/observability/references/gates.md`)
compares first-24h fires with this baseline. Over 3× means the logic is wrong (usually a filter),
not that the business broke. That is why the baseline must be recorded in the registry in events
per day, with its window, before the build.
