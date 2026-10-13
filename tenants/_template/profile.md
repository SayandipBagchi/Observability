# Tenant: `<name>` — profile

*Programme, owner, workspace and delivery for this tenant's MoEngage alerting. Every line was
asked or read in session, never inferred from another tenant.*

**As of `<date>` (rev 1).**

---

## 1 · Programme and owner

- **Programme:** `<programme, product, market>`. Went live `<date>`.
- **Owner:** `<name>`. Approves every alert, threshold and payload before build.
- **Recipients:** held only in `config.json → recipients`.

## 2 · Workspace

- MoEngage `<header name>`, `<Live/Test>`, host `<dashboard-0X>`, confirmed by header read on `<date>`.
- Alert emails label it `<email label>` (same / different: `<evidence>`).
- Other workspaces visible to the account: `<list>`.

## 3 · Delivery paths

- Native alerts: MoEngage email (+ MS Teams: `<yes/no>`).
- Sentinel flows: connector POST to `<intake name>` (owner `<owner>`), which writes `<log>` and feeds
  `<digest / relay>`. Intake URL: never stored.

## 4 · Payload

- uid approved: `<yes/no, date>`. `{{UserAttribute['ID']}}` resolves to `<format, length>` (from the
  first intake row; never the value).
- ref per alert: `ref-table.md`.

## 5 · Baseline convention

30-day average ending on the last day each event fired; window `<from>–<to>`. Stopped processes:
`<list with dates>`.

## 6 · Acquisition

`<live / paused since date>`. Acquisition-dependent alerts: registry column.

## 7 · Sources

- Source sheet: `source/<file>` (`<encoding, rows>`).
- Build log: `<file>`. Flow log: `<location>`.

---

*Sibling files: `journeys.md`, `ref-table.md`, `quirk-evidence.md`, `alert-registry.csv`,
`inventory.md`, `open-items.md`, `revisions.md`.*
