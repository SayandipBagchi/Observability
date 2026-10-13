# The tenant profile

Author: Sayandip Bagchi.

A tenant directory is the live state of one programme's MoEngage alerting: which workspace, which
recipients, which events, which alerts. Nothing in it is portable and nothing in it belongs in a
skill file. This page says how the directory is built; it does not restate the template, because
two copies of a form drift.

**The real template is `${CLAUDE_PLUGIN_ROOT}/tenants/_template/`. Copy the whole folder.**

| File | What it holds | Read it when |
|---|---|---|
| `config.json` | Workspace header and email label, host, env, recipients, intake reference (never the URL), journeys, vocabulary, purity terms, acquisition flag | Every task, first |
| `profile.md` | Programme, owner, delivery paths, uid resolution, baseline convention, acquisition state | Design, onboarding |
| `journeys.md` | Per journey: alerts, events, ref, baselines with as-of dates | Design, health |
| `ref-table.md` | Approved `ref` per alert, or "uid only" with reason | Flow build, A0 |
| `quirk-evidence.md` | Evidence behind each numbered quirk, keyed by number | When a quirk is disputed |
| `intake-rules.md` | Intake rules per alert (burst, daily, cooldown), log columns | Intake work, A6b |
| `alert-registry.csv` | One row per alert ID | Every task |
| `inventory.md` | Paused and replaced objects, TEST alerts, system alerts | Health, retire |
| `open-items.md` | Findings with owner and next action | Health, end of session |
| `revisions.md` | State block and dated change log | When something moved |

Starting one: run `tenant-onboard`. Never copy another tenant's folder and edit it; the copied event
names reconcile perfectly and are wrong.
