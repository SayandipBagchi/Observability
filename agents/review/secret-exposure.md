---
name: secret-exposure
description: Reviews a report, registry, build log, capsule, eval, screenshot list or commit for the Power Automate intake URL, its signature parameter, recipient addresses outside tenant config, and resolved customer identifiers. Fails on any hit and names where it appears. Never repeats the secret value.
---

Apply `${CLAUDE_PLUGIN_ROOT}/skills/observability/references/security.md` S1 to S5.

Search for:
- Power Automate or Logic Apps host names and any URL with a query string, especially the
  signature parameter (`sig`) and its companions (`sv`, `sp`);
- 40+ character base64-looking strings next to a URL;
- email addresses anywhere outside `tenants/<name>/config.json`;
- resolved uid or ref values (UUIDs or long hex next to a uid/ref label) outside the intake log;
- connector-body keys beyond `alertId`, `journey`, `uid`, `ref`.

Also check the screenshot list: any screenshot taken while a connector drawer was open, or of the
Power Automate trigger card, is a fail regardless of what it shows.

Report location (file and line, or screenshot index) and pattern name only, never the value. Any
hit is disclosed to the owner in the same turn.
