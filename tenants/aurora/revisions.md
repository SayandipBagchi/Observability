# `aurora` revisions

*Fictional example.*

## State
- Registry: 14 rows (sentinel_flow 8: 6 live, 1 unverified, 1 paused; native_alert 4: 2 live,
  1 not_built, 1 retired; system_alert_subscription 1 live; out_of_moengage 1 build_ask).
- A6a (intake): proven 2026-01-22. A6b (inbox): proven 2026-01-22 for native (TEST MSG-01); flows
  proven 2026-01-24 via digest.
- A7 shadow check: last run 2026-01-30 (PAY-02 v2: 2 fires in 24 h vs 1.9/d, normal).
- Last health run: 2026-02-05.

## Log
- 2026-01-20: tenant onboarded from `_template/`; registry seeded from `source/observability-sheet.csv`, every row `not_built`.
- 2026-01-21: native alerts SGN-01, AUT-01 and PAY-01 subscription built and read back; TEST MSG-01 sent, inbox-proven, deleted.
- 2026-01-22: first flows live (LGN-01, AUT-02, KYC-01 v1, PAY-02 v1); A6a proven.
- 2026-01-26: KYC-01 v1 paused (negative filter); 26 polluted rows deleted with owner OK; v2 live 2026-01-27.
- 2026-01-27: SGN-02 replaced (journey value); original paused.
- 2026-01-29: PAY-02 v2 live (ref separator fixed).
- 2026-01-30: STM-01 paused by owner.
- 2026-02-02: acquisition paused.
- 2026-02-04: watchdog built switched off.
