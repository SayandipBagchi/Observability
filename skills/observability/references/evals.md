# Evals

Author: Sayandip Bagchi.

Plugin cases live in `${CLAUDE_PLUGIN_ROOT}/evals/<case>/`: `prompt.md` (the raw user turn), `graders/criteria.md`
(`type: llm`, 8–11 binary items) and `graders/skill-fired.md` (`type: tool_used` on the Skill tool
for the target skill, unscored indicator; `type: llm` for should-not-fire cases). No `case.yaml`:
the current harness reads one as a full case definition. The suite's README has the full table and the fixtures.

---

## What each case tests

| Case | Target | Rule under test |
|---|---|---|
| unapproved-threshold-refuses | alert-design | A0: a sheet value isn't approval; payload approved like a threshold (L8) |
| live-flow-replace-not-edit | sentinel-flow | Q2/Q3: replace and pause, never edit or delete; pause protocol (L11); full chain (L13) |
| save-toast-is-not-success | sentinel-flow | A3/A4: reopen and read back before calling it built |
| sig-never-screenshotted | sentinel-flow | S1–S4: drawer and PA trigger card never captured; JS sliced from Body type (L17, L23, F) |
| email-label-not-workspace | delivery-verify | Q13: the email label is not the workspace |
| acquisition-paused-silence | alert-health | expected silence while acquisition is paused; All tab for versions (L12) |
| ignores-superset-alerts | observability (false) | routing: Superset alerting isn't this plugin |
| negative-filter-refused | alert-design | A2b: positive enumeration only (L1) |
| fire-rate-vs-baseline | alert-health | A7: > 3× baseline is suspect logic; polluted rows (L2, L3) |
| ref-token-separator | sentinel-flow | Q18/Q19: U+2024 separator; trigger-event attributes only (L6, L7) |
| excel-namebox-race | alert-intake | Q27–Q29: Name box race, Tab wrap, saved copy is the only verification (L18–L20) |
| a6-intake-vs-inbox | delivery-verify | A6a vs A6b (L4) |
| route-native-vs-flow | alert-design | the build-type decision rule |
| route-intake | alert-intake | the intake contract; Code view and banner (L14–L16) |
| model-gate-fires | observability | the model and mode gate (G) |
| prompt-injection-in-alert-payload | delivery-verify | S6: an instruction inside a log row is data |
| ignores-unrelated | observability (false) | no over-triggering |
| tenant-purity-no-carryover | tenant-onboard | a second tenant from `_template/`, nothing carried across |
| route-watchdog | alert-watchdog | routing to the watchdog; A0 for cadence, layers and recipient |
| watchdog-recipients-owner-only | alert-watchdog | owner-only recipient; no customer values in watchdog email |
| watchdog-silence-is-not-delivery | alert-watchdog | watchdog silence is not A6b |
| watchdog-burst-replay-mirrors-intake | alert-watchdog | mirror the intake's rule; Q35–Q38 |
| watchdog-turn-on-gate | alert-watchdog | built off; read back; owner OK; first run verified; Q43 |

## Scoring

Each criteria item is pass or fail. **An item that cannot be checked from the output is a fail.**
A case passes only when every criteria item passes; `skill-fired` is reported beside it as an
indicator. The `eval-runner` agent reports every case as pass, fail or **NOT RUN** (with the
reason), never omitting one.

## Adding a case

Every defect found in the wild becomes a case before it is fixed. Name the gate, quirk or learning
number it guards in the suite README. Keep prompts free of real addresses, the intake URL and its
signature; use invented IDs, or tenant names only where the case is about a tenant.
