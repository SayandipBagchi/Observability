# `aurora` ref table

*Fictional example. The approved `ref` per sentinel flow, or "uid only" with the reason. Each row
is an A0 approval, like a threshold. Stored notation uses ASCII dots; the live token uses U+2024.*

| Alert | Journey | Trigger event | ref (stored notation) | Identifies | uid-only reason | Approved (who, when) | Flow ID |
|---|---|---|---|---|---|---|---|
| LGN-01 | login | `ac_code_sent` | `MOE_TRIGGER_EVENT.ac_code_sent.ac_application_ref` | the application | | owner, 2026-01-21 | 000000000000000000a0f101 |
| SGN-02 | signup | `ac_signup_started` | — | | trigger carries only a session-scoped ID, which cannot be personalised | owner, 2026-01-21 | 000000000000000000a0f202 |
| KYC-01 | kyc | `ac_idcheck_failed` | `MOE_TRIGGER_EVENT.ac_idcheck_failed.ac_application_ref` | the application | | owner, 2026-01-21 | 000000000000000000a0f301 |
| KYC-03 | kyc | `ac_idcheck_started` | `MOE_TRIGGER_EVENT.ac_idcheck_started.ac_application_ref` | the application | | owner, 2026-01-23 | (unverified) |
| KYC-05 | card | `ac_application_status` | `MOE_TRIGGER_EVENT.ac_application_status.ac_application_ref` | the application | | owner, 2026-01-24 | 000000000000000000a0f305 |
| AUT-02 | auth | `ac_auth_result` | `MOE_TRIGGER_EVENT.ac_auth_result.ac_auth_ref` | the authorisation | | owner, 2026-01-21 | 000000000000000000a0f402 |
| PAY-02 | payment | `ac_payment_started` | `MOE_TRIGGER_EVENT.ac_payment_started.ac_payment_ref` | the payment | | owner, 2026-01-22 | 000000000000000000a0f502 |
| STM-01 | statement | `ac_statement_ready` | — | | low value; uid is enough to find the statement | owner, 2026-01-24 | 000000000000000000a0f601 |

## Changing a row

A new ref is a new A0 approval and a flow replacement (live flows are never edited). Record the
replaced ID in the registry's `replaced_ids` chain.
