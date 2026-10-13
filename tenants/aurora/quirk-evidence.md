# `aurora` quirk evidence

*Fictional example. The evidence behind each generic quirk or gate as it would be recorded on a
tenant, keyed by the number in `skills/observability/references/designer-quirks.md` and
`gates.md`. Evidence only; rules live in the skills. Every date and ID here is invented.*

| # | Evidence (date, alert, object ID, what happened) |
|---|---|
| Q13 | 2026-01-21: SGN-01 email arrived labelled `Aurora_Sandbox`; header read showed `Aurora_Live`. Alert found Active in the `Aurora_Live` list. Nothing deleted. |
| Q18 | 2026-01-28: PAY-02 v1 (`…f1b2`) ref token typed with a full stop; 4 intake rows with blank Ref. Replaced by v2 (`…f502`) with U+2024; v1 paused. |
| Q2 / Q3 | 2026-01-27: SGN-02 journey value wrong on the live flow. Duplicated, renamed by canvas click, fixed, read back, published; original (`…f1a2`) paused. Rows kept (cosmetic fix). |
| A2b / Q23 | 2026-01-26: KYC-01 v1 (`…f1b1`) qualified on `ac_status_label` is not empty: fired on APPROVED too. 26 fires in first 24 h vs baseline 5.4/d. Paused, replaced with a positive enumeration; 26 polluted rows deleted with owner OK. |
| A3 / Q4 | 2026-01-23: KYC-03 showed the Saved toast; reopen not yet done. Registry row held at `unverified`. |
| A6a | 2026-01-22: first intake rows for AUT-02 with Uid and Ref populated. |
| A6b | 2026-01-22: TEST MSG-01 email received with matching subject, label and data window; alert deleted within 24 h. |
| Q22 | 2026-01-30: `filter_block=paused` errored; STM-01 found by searching the ID and opening the All tab. |
| S3 / S4 | No incidents. Connector bodies read by JS from Body type down; no drawer screenshots. |
| Q35 | 2026-02-04: watchdog burst replay compared counts with equality and missed a burst of 3 at threshold 3; fixed to ≥ with older rows + 1. |
