# Tenant: `aurora` — profile

*Fictional example tenant. Aurora Card is an invented demo programme: every name, address, event,
ID, date and number in this folder is made up to show what a filled-in tenant looks like.*

**As of 2026-02-06 (rev 3).**

---

## 1 · Programme and owner

- **Programme:** Aurora Card, a fictional consumer credit card used as a demo. Went live 2026-01-12.
- **Owner:** the card owner (fictional). Approves every alert, threshold and payload before build.
- **Recipients:** held only in `config.json → recipients` (three `example.com` addresses).

## 2 · Workspace

- MoEngage `Aurora_Live`, Live, host `dashboard-0X`, confirmed by header read on 2026-01-20.
- Alert emails label it `Aurora_Sandbox` (different from the header: the label is the workspace's
  internal name, not where the alert lives; see quirk Q13 in `quirk-evidence.md`).
- Other workspaces visible to the account: `Aurora_Sandbox` (QA workspace; alerts are built in `Aurora_Live` only).

## 3 · Delivery paths

- Native alerts: MoEngage email + MS Teams (via the chat relay flow).
- Sentinel flows: connector POST to the Aurora Alert Intake (owner: card owner), which writes the
  AlertLog tab of `aurora_alert_log.xlsx` and feeds a daily digest and the chat relay. Intake URL:
  never stored.

## 4 · Payload

- uid approved: yes, 2026-01-21. `{{UserAttribute['ID']}}` resolves to MoEngage's own 24-hex user ID
  (format read from the first intake row; the value is never stored).
- ref per alert: `ref-table.md`.

## 5 · Baseline convention

30-day average ending on the last day each event fired; window 2026-01-04 to 2026-02-03 for flows,
2026-01-01 to 2026-01-31 for native volumes. Stopped processes: none.

## 6 · Acquisition

Paused since 2026-02-02 (marketing pause, fictional). Acquisition-dependent alerts are marked in the
registry; expect silence on them until acquisition resumes.

## 7 · Sources

- Source sheet: `source/observability-sheet.csv` (UTF-8, 14 rows).
- Build log: `build_log.csv`. Flow log: same file.

---

*Sibling files: `journeys.md`, `ref-table.md`, `quirk-evidence.md`, `alert-registry.csv`,
`inventory.md`, `open-items.md`, `revisions.md`, `intake-rules.md`.*
