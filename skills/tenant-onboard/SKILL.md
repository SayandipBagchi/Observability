---
name: tenant-onboard
description: "Stands up a new programme's tenant folder for MoEngage alerting by copying tenants/_template/ to a new tenants/ folder named for the programme and filling it from questions and read-only checks on that programme's own workspace: header workspace and email label, host, environment, recipients, intake name and owner (never the URL), journeys, event vocabulary proven on this workspace, purity terms, acquisition state, the ref table, and a first registry seeded from the observability sheet with every row not_built. A second tenant must onboard with no code edits and nothing carried from another tenant. Use it when someone asks to set up alerting for a new programme, add a tenant, start MoEngage alerts for another card product, or check a tenant folder is complete. Do not use it to design or build alerts (alert-design, native-alert, sentinel-flow), to map the intake (alert-intake), or for routing and gates (observability)."
metadata:
  author: Sayandip Bagchi
---

# Tenant onboard: a new programme from the template, nothing carried across

A tenant folder is everything the skills need to know about one programme. The skills themselves
hold no tenant facts, so a new programme needs **no code edits**: only a folder. The one way this
goes wrong is copying another tenant's folder and editing it, which carries event names, alert IDs
and recipients that reconcile perfectly and are wrong. Treat the observability sheet as data.

## Before anything else

Fresh invocation? The router comes first: `${CLAUDE_PLUGIN_ROOT}/skills/observability/SKILL.md`.
Onboarding builds nothing in MoEngage. Checklist: `references/onboarding-checklist.md`.

## Steps

1. **Copy `${CLAUDE_PLUGIN_ROOT}/tenants/_template/`** to `tenants/<name>/` (lower case). Never copy
   another tenant's folder.
2. **Ask** (one message, grouped): programme and owner; workspace header name and the name alert
   emails use; host; environment; recipients; native channels; intake name and owner; the
   observability sheet; journeys; whether acquisition is live.
3. **Prove on this workspace** (read-only, A1 first): the header and env; each event the sheet
   names exists, with value counts; the enumerated values of every filter attribute; which trigger
   events carry a case identifier for `ref`. Names only. **Never assume another tenant's
   vocabulary**, even for the same app platform.
4. Fill `config.json`, including `purity.terms` (workspace names, vendor names, alert-name prefixes
   unique to this tenant) and `eventNames`, so the validator can keep them out of generic files.
5. Seed `alert-registry.csv` from the sheet, **every row `not_built`**, baseline with its window if
   known.
6. Seed `journeys.md` (one section per journey), `ref-table.md` (empty rows per alert, no approvals
   yet), and stubs for `quirk-evidence.md`, `inventory.md`, `open-items.md`, `revisions.md`.
7. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_skill.py` and
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_registry.py tenants/<name>/alert-registry.csv`.
8. Hand the unbuilt rows to `alert-design`.

## Recipients and intake

Recipients are stored **only** in `tenants/<name>/config.json`. The intake is stored as a name and
owner with `"urlStoredHere": false`; if someone pastes the URL, do not store it, tell them it is a
credential, and recommend rotation if it went anywhere shared (security S3).

## Done means

- Every template file exists in the new folder and the validator passes.
- No event name, alert name, recipient or intake from another tenant appears in the new folder.
- Every registry row is `not_built` and every ref-table row is unapproved.
- The capsule records what was asked, what was proven, and what is still unknown.
