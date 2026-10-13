# Observability

Author: Sayandip Bagchi. Version lives in `.claude-plugin/plugin.json`. Licence: MIT.

A Claude plugin for **real-time business alerting built inside MoEngage**, multi-tenant by
construction. It turns an observability sheet into approved alerts, builds them in the browser,
proves they were delivered, audits what is live and watches for alerts that silently stopped.

> **Demo repository.** This is a public, sanitised edition. The example tenant in `tenants/` is
> entirely fictional: every programme name, address, event, ID, date and number in it is invented.
> Not affiliated with or endorsed by MoEngage, Microsoft or any card programme.

Two build types do the work:

- **Native alerts** (Alert Management: Events Volume, Campaign Stats, system-alert subscriptions)
  evaluate an aggregate over a data window and email the recipients directly.
- **MON sentinel flows** are silent flows that watch one journey step and, for each broken trip,
  POST `{alertId, journey, uid[, ref]}` to a Power Automate intake, which logs a row in AlertLog
  and feeds the digest to Outlook.

## Why it exists: the guardrails

Alerting goes quietly wrong in predictable ways. Each of these is a gate the plugin enforces, with
an eval case behind it:

- **Nothing is built without in-session approval** of the alert, threshold or wait, recipients and
  payload. A sign-off in a spreadsheet is context, not approval.
- **Filters are positive enumerations.** An `is not empty` filter fires on successes.
- **Every save is read back from the persisted state.** A green toast is not success.
- **Live flows are replaced, never edited**, and the full replace chain is kept.
- **Intake proof and inbox proof are separate.** A log row is not an email in someone's inbox.
- **First-24h shadow check:** more than 3× baseline on day one is suspect logic, not an incident.
- **The intake URL and its signature never land anywhere**: no screenshots of connector drawers or
  trigger cards, JS reads sliced, output masked.
- **Tenants are pure:** every programme fact lives in `tenants/<name>/`; skills stay generic.

## Skills

**`observability`** The router and the governor. Runs the model gate (which model, plan vs
direct), resolves the tenant, holds gates A0 to A7 and the security rules, and routes. It never
builds anything itself.

| Skill | Owns |
|---|---|
| `alert-design` | Sheet row → spec; native vs flow decision rule; baseline; fire-rate estimate; approval table |
| `native-alert` | Alert Management create and read-back; schedule and data window; recipients from config; system-alert subscriptions |
| `sentinel-flow` | MON flow build and replace; NO branch only; connector body; uid/ref tokens with the U+2024 separator; positive filters |
| `alert-intake` | Power Automate Parse JSON schema, AlertLog columns, Code-view mapping check; workbook, sheet and doc read-back quirks |
| `delivery-verify` | A6a intake proof vs A6b inbox proof; TEST alert lifecycle |
| `alert-health` | Registry vs live; silent, noisy, orphaned; the A7 first-24h shadow check |
| `alert-retire` | Pause protocol; full `replaced_ids` chain; polluted-row cleanup with owner OK |
| `alert-watchdog` | Power Automate watchdog: missed-burst replay from the log, failure catches on intake/relay/digest, daily silence check; owner-only, built off, read back |
| `tenant-onboard` | A new programme from `tenants/_template/`, with no code edits |

## Layout

```tree
observability/
├── .claude-plugin/plugin.json   # name, version and author, declared once
├── agents/                      # 8 subagents, including builders/ and review/
├── skills/                      # 10 skills, each with its own references/
├── tenants/                     # _template/ plus one fictional example tenant
├── evals/                       # 23 cases with graders, plus fixtures
├── hosts/openai.yaml            # optional UI metadata, no behaviour
├── scripts/                     # validate_skill.py, validate_registry.py, leak_scan.py
├── .githooks/pre-commit         # runs the leak scan and the package validator
├── hooks/hooks.json             # session-start reminder of the gates (declared extra)
├── settings.json                # generic defaults; no tenant (declared extra)
└── CONNECTORS.md                # what each skill reaches and how (declared extra)
```

No `commands/`: the six former commands are now skills with trigger descriptions. Skills, agents,
hooks, settings and this README are tenant-clean; every programme-specific fact, including
recipients, lives under `tenants/<name>/`.

## Install

```bash
git clone https://github.com/SayandipBagchi/observability.git
```

Add the cloned folder as a plugin in Claude (or Claude Code). The ten skills and eight agents
register together. To try it, read the fictional example tenant under `tenants/`, then onboard
your own programme with the `tenant-onboard` skill.

## Use

The router fires on anything that sets up, builds, verifies, audits or retires MoEngage alerting,
or asks which skill or tenant a request belongs to. It runs the model gate first on any live work.
Sub-skills fire on their own vocabulary and hand off at their stated boundaries.

## Requirements

Claude in Chrome, signed in to the tenant's MoEngage workspace, Power Automate (for intake work)
and Outlook web. No MCP server ships with the plugin. See `CONNECTORS.md`.

## Tenants

`tenants/<name>/` holds `config.json`, `profile.md`, `journeys.md`, `ref-table.md`,
`quirk-evidence.md`, `intake-rules.md`, `alert-registry.csv`, `inventory.md`, `open-items.md`, `revisions.md` and
`source/`. Start a new programme with the `tenant-onboard` skill from `tenants/_template/`, never by
copying another tenant. See `tenants/README.md`.

## Checking the package

```bash
python3 scripts/validate_skill.py
python3 scripts/validate_registry.py tenants/<name>/alert-registry.csv
```

`validate_skill.py` checks the manifest, every skill's frontmatter, description ceiling, markers
and required references, links and the `${CLAUDE_PLUGIN_ROOT}` cross-skill rule, the learnings
trace, tenant purity across every generic file, a secret scan across the whole package, each
tenant's full file set, agent frontmatter against the declared list, the eval case structure, the
root files and declared extras, `hosts/openai.yaml`, and that `commands/` does not exist.
`validate_registry.py` checks a registry's columns, enums, IDs, replace chains, positive
enumeration on live flows, payload decisions, and that no URL, signature or email address sits in
any cell.

## Keeping private data out (leak guard)

Real tenant folders are git-ignored; only `tenants/README.md`, `tenants/_template/` and the
fictional example ship. Two guards stop private material reaching a commit:

1. **`.private-denylist`** (untracked, never committed): one private term per line, such as an
   employer name, a programme name, a vendor or a real event name. Lines starting with `re:` are
   regexes. `validate_skill.py` reads it for tenant purity and email domains, so the guard code
   itself names nothing private.
2. **`scripts/leak_scan.py`** checks every file (or only staged files with `--staged`) against the
   denylist, secret and intake-host patterns, non-allowlisted URLs and any email domain other than
   `example.com`, `example.org` or `example.invalid`. It reports file, line and rule, and never
   prints the matched text.

Enable the hook once per clone:

```bash
git config core.hooksPath .githooks
```

## Licence

MIT. See `LICENSE`.
