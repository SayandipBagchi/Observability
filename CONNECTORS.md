# Connectors

What each skill needs to reach, and how. No MCP server ships with this plugin; MoEngage alert
management and flows have no API in use here, so live work runs through a signed-in browser.

| Need | Used | Skills | Notes |
|---|---|---|---|
| MoEngage dashboard (Alert Management, Flows, Data Management) | Claude in Chrome, signed-in session | native-alert, sentinel-flow, alert-health, alert-retire, tenant-onboard | Read connector bodies via JS sliced from "Body type"; never screenshot a drawer |
| Power Automate intake | Claude in Chrome, signed-in session | alert-intake | Actions below the trigger only; never expand or capture the trigger card. URL and signature are never stored |
| Intake log (AlertLog workbook) | Excel Online via Chrome; saved-copy download for read-back | alert-intake, delivery-verify, alert-health | The saved copy, not the screen, is evidence |
| Alert delivery check | Outlook web via Chrome | delivery-verify | Search by alert name; match the data window |
| Flow log, handoff docs, status sheets | Google Drive (read), Google Docs / Sheets via Chrome | alert-intake | Verify via Drive read-back and CSV export |
| Registry and tenant files | Local files in `tenants/<name>/` | all | Validated by `scripts/validate_registry.py` |

Each tenant's `config.json` names its own workspace, intake and log locations. This file names
none.

## Watchdog

| Surface | How | Skill | Rule |
|---|---|---|---|
| Power Automate (watchdog flow, failure catches on intake/relay/digest) | Claude in Chrome, signed-in session; new designer, Code view read-back | alert-watchdog | Never open the intake trigger card; the watchdog only reads the rules and log tables and emails the owner |
