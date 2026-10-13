# `aurora`: live journey state

*Fictional example. Per journey: the alerts, trigger events, filters, payload ref and baselines.
Every figure is invented and carries its own as-of window.*

---

## `login`

Sign-in by one-time code.

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| LGN-01 | P2 | sentinel_flow | `ac_code_sent` with Alert Name = `Aurora sign-in code` → NO `ac_code_verified` | 10 min | application ref | 3.8/d (0–11) · 01-04–02-03 | live | no |

**Vocabulary proven on this workspace (2026-01-20):** `ac_code_sent`, `ac_code_verified`, `ac_code_resend`.

---

## `signup`

Application start to submit.

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| SGN-01 | P2 | native_alert | `ac_signup_started` volume down > 40% vs previous 7 days | Daily 06:50 UTC | — | 63/d (41–88) · 01-01–01-31 | live | yes |
| SGN-02 | P3 | sentinel_flow | `ac_signup_started` → NO `ac_signup_submitted` | 45 min | uid only | 9.1/d (3–17) · 01-04–02-03 | live (v2) | yes |
| SGN-04 | P2 | native_alert | approval rate < 65% / day (sheet) | Daily | — | 58% (49–67%) · 01-04–02-03 | not_built | yes |

**Vocabulary proven (2026-01-20):** `ac_signup_started`, `ac_signup_submitted`.

---

## `kyc`

Identity check.

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| KYC-01 | P1 | sentinel_flow | `ac_idcheck_failed` with `ac_status_label` in [DOC_BLURRED, DOC_EXPIRED, FACE_MISMATCH] | every event | application ref | 5.4/d (1–12) · 01-04–02-03 | live (v2) | yes |
| KYC-03 | P2 | sentinel_flow | `ac_idcheck_started` → NO `ac_idcheck_passed` | 30 min | application ref | 2.2/d (0–7) · 01-04–02-03 | unverified | yes |

**Vocabulary proven (2026-01-20):** `ac_idcheck_started`, `ac_idcheck_passed`, `ac_idcheck_failed`;
`ac_status_label` values DOC_BLURRED (61), DOC_EXPIRED (24), FACE_MISMATCH (37), APPROVED (1,140).

---

## `card`

Approval to card in hand.

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| KYC-05 | P2 | sentinel_flow | `ac_application_status` with `ac_status_label` in [APPROVED] → NO `ac_card_shipped` | 2 d | application ref | 0.4/d (0–2) · 01-04–02-03 | live | yes |

**Vocabulary proven (2026-01-20):** `ac_card_shipped`, `ac_card_activated`, `ac_pin_set`.

---

## `auth`

Card authorisations.

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| AUT-01 | P1 | native_alert | `ac_auth_result` < 120 in last Day | Daily 06:50 UTC | — | 410/d (260–590) · 01-01–01-31 | live | no |
| AUT-02 | P1 | sentinel_flow | `ac_auth_result` with `ac_decline_code` in [AC_SYSTEM_FAULT] | every event | auth ref | 1.3/d (0–5) · 01-04–02-03 | live | no |

---

## `payment`

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| PAY-01 | P2 | system_alert_subscription | connector failure-rate breach | MoEngage schedule | — | — | live | no |
| PAY-02 | P2 | sentinel_flow | `ac_payment_started` → NO `ac_payment_settled` | 3 h | payment ref | 1.9/d (0–6) · 01-04–02-03 | live (v2) | no |

---

## `statement`

| ID | Sev | Build type | Trigger (positive filters) | Wait / cadence | ref | Baseline (window) | Status | Acq. |
|---|---|---|---|---|---|---|---|---|
| STM-01 | P3 | sentinel_flow | `ac_statement_ready` → NO `ac_statement_opened` | 5 d | uid only | 22/d (9–40) · 01-04–02-03 | paused | no |
