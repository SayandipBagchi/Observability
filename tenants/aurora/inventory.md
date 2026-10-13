# `aurora` MoEngage inventory (as of 2026-02-05, fictional)

## Live
- 6 MON flows (LGN-01, SGN-02 v2, KYC-01 v2, KYC-05, AUT-02, PAY-02 v2), 2 native alerts (SGN-01,
  AUT-01), 1 system-alert subscription (PAY-01). KYC-03 saved, not yet read back.

## Paused (replaced originals; never delete)
| Alert ID | Paused ID | Reason | Replacement |
|---|---|---|---|
| SGN-02 | 000000000000000000a0f1a2 | journey value wrong (cosmetic) | 000000000000000000a0f202 |
| KYC-01 | 000000000000000000a0f1b1 | negative filter fired on approved checks | 000000000000000000a0f301 |
| PAY-02 | 000000000000000000a0f1b2 | ref separator was a full stop | 000000000000000000a0f502 |
| STM-01 | 000000000000000000a0f601 | paused by owner, low value | — |

## TEST alerts
| Name | Evidence | State |
|---|---|---|
| TEST MSG-01 delivery check | inbox email matched 2026-01-22 | deleted 2026-01-22 |
