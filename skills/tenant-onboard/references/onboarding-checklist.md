# Onboarding checklist

Author: Sayandip Bagchi.

Every row is asked or proven, never inferred from another tenant.

---

## Asked

| # | Question | Lands in |
|---|---|---|
| 1 | Programme name, product, go-live date | `profile.md` |
| 2 | Owner who approves alerts, thresholds and payloads | `profile.md` |
| 3 | Workspace header name, and the name alert emails show | `config.json → moengage` |
| 4 | Host (`dashboard-0X`), environment (Live/Test) | `config.json → moengage` |
| 5 | Recipients (full addresses) | `config.json → recipients` only |
| 6 | Native channels (Email, MS Teams) and Teams channel | `config.json` |
| 7 | Intake name and owner; does it stamp receipt time and under what column | `config.json → intake` |
| 8 | Journeys (connector `journey` values) | `config.json → journeys`, `journeys.md` |
| 9 | Observability sheet (file, owner, version) | `source/`, `profile.md` |
| 10 | Is acquisition live? If paused, since when | `config.json → acquisitionPaused` |
| 11 | Are uid payloads approved on this tenant? Which user attribute is the customer key | `profile.md`, `config.json → connectorBodyKeys` |
| 12 | Flow log / build log location | `config.json → flowLog` |

## Proven (read-only, on this workspace)

| # | Check | How | Lands in |
|---|---|---|---|
| 1 | A1: header and env | JS read of the header | `revisions.md` |
| 2 | Each sheet event exists | Data Management or a recent occurrence | `journeys.md`, `config.json → eventNames` |
| 3 | Enumerated values of each filter attribute, with counts | event attribute breakdown | `journeys.md` |
| 4 | OTP SMS alert names (if SMS alerts are in scope) | transactional alert list | `config.json → vocabulary` |
| 5 | Which trigger events carry a case identifier | personalisation picker on a draft flow, not saved | `ref-table.md` (unapproved) |
| 6 | Existing alerts and flows, system alerts | Alert Management and Flows lists | `inventory.md` |
| 7 | Other workspaces visible to the account | workspace switcher | `config.json → moengage.otherWorkspacesSeen` |

## Purity terms

Fill `config.json → purity.terms` with strings unique to this tenant that must never appear in a
generic file: workspace names, vendor names used in event names, OTP alert-name prefixes. The
validator also bans every entry in `eventNames` and every string under `vocabulary`.

## Files the new folder must contain

`config.json`, `profile.md`, `journeys.md`, `ref-table.md`, `quirk-evidence.md`,
`intake-rules.md`, `alert-registry.csv`, `inventory.md`, `open-items.md`, `revisions.md`, and `source/` for the sheet
as received. The validator fails a tenant folder missing any of the first ten.
