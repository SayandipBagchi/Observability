# Learnings trace

Author: Sayandip Bagchi.

Where each learning landed: the payload rollout learnings (L1–L23, F, G), the workbook learnings
(L24–L26) and the watchdog learnings (L27–L32). A tenant may archive its own session notes under
`tenants/<tenant>/source/`; none ship with this repo. Each row names the primary
file (relative to the plugin root) and an **anchor**: a literal string in that file that
`scripts/validate_skill.py` checks is still present, so a later edit cannot silently drop a
guardrail. Evidence for each learning stays in the tenant's `quirk-evidence.md`.

| # | Learning | Primary file | Anchor | Also in | Eval |
|---|---|---|---|---|---|
| L1 | Negative / "is not empty" filters let successes through; filters are positive enumerations | `skills/observability/references/gates.md` | `A2b positive enumeration` | designer-quirks Q23; sentinel-flow/references/flow-build.md; validate_registry.py | negative-filter-refused |
| L2 | First-24h shadow check: fires vs baseline; > 3× = suspect logic, not incident | `skills/observability/references/gates.md` | `A7 shadow check` | alert-health/references/health-checks.md; agents/shadow-triangulator.md | fire-rate-vs-baseline |
| L3 | Rows written by a logic-wrong flow are polluted; delete with owner OK and record the count | `skills/observability/references/run-protocol.md` | `## Polluted rows` | alert-retire/references/retire-protocol.md; tenant revisions | fire-rate-vs-baseline |
| L4 | AlertLog proves MoEngage → intake only; inbox is a separate hop | `skills/observability/references/gates.md` | `A6a intake-proven` | delivery-verify/references/delivery-proof.md | a6-intake-vs-inbox |
| L5 | uid token `{{UserAttribute['ID']}}`; what it resolves to is tenant-specific | `skills/observability/references/designer-quirks.md` | `Q17` | sentinel-flow/references/payload-tokens.md; tenant profile | ref-token-separator |
| L6 | ref token separator is U+2024, not a full stop | `skills/observability/references/designer-quirks.md` | `Q18` | sentinel-flow/references/payload-tokens.md; registry-schema | ref-token-separator |
| L7 | Only trigger-event attributes are personalisable; session IDs are not; ref may be blank with a reason | `skills/observability/references/registry-schema.md` | `may be blank, with a reason` | designer-quirks Q19 | ref-token-separator |
| L8 | Per-alert ref is approved like a threshold (A0) | `skills/observability/references/gates.md` | `is approved exactly like a threshold` | alert-design/references/design-rules.md | unapproved-threshold-refuses |
| L9 | uid + approved ref are allowed in payloads; nothing else | `skills/observability/references/security.md` | `S5 · Customer data in alert payloads` | sentinel-flow SKILL.md | sig-never-screenshotted |
| L10 | Screenshot frame vs CSS viewport; re-screenshot before coordinate clicks; discard a wrongly touched draft | `skills/observability/references/designer-quirks.md` | `Q20` | run-protocol Session hygiene | live-flow-replace-not-edit |
| L11 | Pause only after load, only with the dialog, confirm in list view | `skills/observability/references/run-protocol.md` | `## Pause protocol` | designer-quirks Q21 | live-flow-replace-not-edit |
| L12 | `filter_block=paused` errors; use search + All tab | `skills/observability/references/designer-quirks.md` | `Q22` | alert-retire/references/retire-protocol.md | acquisition-paused-silence |
| L13 | Replace chains pass v2; `replaced_ids` keeps the full `;` chain | `skills/observability/references/registry-schema.md` | `## The replace chain` | validate_registry.py | live-flow-replace-not-edit |
| L14 | Parse JSON schema commits only after click-out and re-render | `skills/observability/references/designer-quirks.md` | `Q24` | alert-intake/references/power-automate.md | route-intake |
| L15 | Expression fallback `body('Parse_JSON')?['<key>']`; popup must be open | `skills/observability/references/designer-quirks.md` | `Q25` | alert-intake/references/power-automate.md | route-intake |
| L16 | Verify mappings in Code view; require "Your flow is ready" | `skills/observability/references/gates.md` | `Code view` | designer-quirks Q26 | route-intake |
| L17 | Never expand or screenshot the PA trigger card | `skills/observability/references/security.md` | `Power Automate trigger card` | designer-quirks S3 | sig-never-screenshotted |
| L18 | Excel Online Name box race; confirm Name box, diff against baseline | `skills/observability/references/designer-quirks.md` | `Q27` | alert-intake/references/sheet-sync.md | excel-namebox-race |
| L19 | Excel saved copy lags the UI and is the only valid verification | `skills/observability/references/gates.md` | `saved copy` | designer-quirks Q28 | excel-namebox-race |
| L20 | Tab inside an Excel table wraps to the next row | `skills/observability/references/designer-quirks.md` | `Q29` | alert-intake/references/sheet-sync.md | excel-namebox-race |
| L21 | Google Sheets Cmd+J = Name box; verify via CSV export | `skills/observability/references/designer-quirks.md` | `Q30` | alert-intake/references/sheet-sync.md | excel-namebox-race |
| L22 | Google Docs: Cmd+Down, autocorrect, italic carry-over; Drive read-back | `skills/observability/references/designer-quirks.md` | `Q31` | alert-intake/references/sheet-sync.md | save-toast-is-not-success |
| L23 | Chrome JS output filter; mask before returning | `skills/observability/references/run-protocol.md` | `## JS output masking` | designer-quirks Q32; security S2 | sig-never-screenshotted |
| L24 | Excel Online active sheet can change between batches; use sheet-qualified Name-box addresses and read back the first cell of each batch | `skills/observability/references/designer-quirks.md` | `Q33` | alert-intake/references/sheet-sync.md; alert-intake SKILL.md | excel-namebox-race |
| L25 | Bulk undo is not a restore; restore cell by cell from the baseline and flag uncaptured prior values for Version History | `skills/alert-intake/references/sheet-sync.md` | `Bulk undo` | designer-quirks Q34 | excel-namebox-race |
| L26 | Alert descriptions follow one four-part format; daily thresholds read "more than N", burst "N or more within X"; baselines come from the live intake rules | `skills/observability/templates/alert-description.md` | `more than N in a day` | alert-intake/references/sheet-sync.md | excel-namebox-race |
| L27 | The intake's burst count can miss the current event (read-after-write); count older rows + 1 | `skills/alert-watchdog/references/watchdog-quirks.md` | `Q35` | alert-watchdog/references/watchdog-build.md | watchdog-burst-replay-mirrors-intake |
| L28 | A missed alert looks like a quiet day; a watchdog replays the intake's rule, catches flow failures and flags silence, owner-only | `skills/alert-watchdog/SKILL.md` | `owner only` | router routing table | route-watchdog |
| L29 | Watchdog silence is not delivery proof | `skills/alert-watchdog/SKILL.md` | `Watchdog silence is not delivery` | router read-first list | watchdog-silence-is-not-delivery |
| L30 | `createArray()` with no arguments fails at run time; integer division truncates; float literals rejected | `skills/alert-watchdog/references/watchdog-quirks.md` | `Q38` | watchdog-build.md | watchdog-burst-replay-mirrors-intake |
| L31 | The platform's weekly failure summary lists fixed failures for 7 days and is not the watchdog | `skills/alert-watchdog/references/watchdog-quirks.md` | `Q43` | alert-watchdog SKILL.md guardrails | watchdog-turn-on-gate |
| L32 | Excel Online can ignore synthetic input; owner edits by hand, then read back | `skills/alert-watchdog/references/watchdog-quirks.md` | `Q44` | alert-intake/references/sheet-sync.md | excel-namebox-race |
| F | Sig surfaced via a whole-drawer JS read and a drawer screenshot; slice from "Body type", no screenshot with a drawer open | `skills/observability/references/security.md` | `slice every JS read from the` | designer-quirks S4; tenant quirk-evidence (incident detail) | sig-never-screenshotted |
| G | Ask plan vs direct and model first; new session after 7–8 prompts; capsule; offer a YAML .md; build log per flow | `skills/observability/references/run-protocol.md` | `## Session hygiene` | router SKILL.md model gate; gates.md A5 | model-gate-fires |

No learning was left unplaced.
