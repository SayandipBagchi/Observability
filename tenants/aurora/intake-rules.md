# `aurora` intake rules

*Fictional example. Source: `aurora_alert_log.xlsx` saved copy, read 2026-02-05, read-only.
Snapshot until re-read. Generic rule model: `skills/alert-intake/references/power-automate.md`,
"The intake rule model".*

## Rules tab (per alert)

| Alert | Sev | BurstCount | BurstWindowMin | DailyThreshold | CooldownMin | Paths on | Note |
|---|---|---|---|---|---|---|---|
| LGN-01 | P2 | 6 | 30 | 15 | 120 | burst, daily | |
| SGN-02 | P3 | — | — | 20 | 1440 | daily | |
| KYC-01 | P1 | 3 | 20 | 12 | 60 | burst, daily | |
| KYC-03 | P2 | 4 | 60 | 9 | 240 | burst, daily | flow unverified |
| KYC-05 | P2 | — | — | 3 | 1440 | daily | |
| AUT-02 | P1 | 2 | 15 | 5 | 30 | burst, daily | |
| PAY-02 | P2 | 3 | 60 | 7 | 180 | burst, daily | |
| STM-01 | P3 | — | — | — | — | off | flow paused |

Recipients configured in the rules: 3, matching `config.json`.

## AlertLog columns

| Column | Meaning |
|---|---|
| A ReceivedSerial | Excel serial (UTC days since 1899-12-30) stamped by the intake on receipt |
| B AlertID | `alertId` from the connector body |
| C Journey | `journey` from the connector body |
| D Severity | looked up from the Rules tab |
| E Path | burst / daily / none |
| F Uid | `uid` from the body (never copied into emails) |
| G Ref | `ref` from the body, blank where the flow is uid only |

## EmailLog columns

| Column | Meaning |
|---|---|
| A SentSerial | when the digest or burst email was sent |
| B AlertID | alert that caused it |
| C Path | burst / daily |
| D RowsCounted | rows counted for the rule |
