# Portability: what travels, what degrades, what is required

Author: Sayandip Bagchi.

---

## The minimum runtime contract

**Only the router `SKILL.md` is strictly required.** It carries the model gate, the gate table in
one-line form, the routing table and the never-do list. Everything else is depth, and a missing
file degrades gracefully in one precise sense: **say what you could not read; never guess what it
said.**

Two absences are blocking, because proceeding produces a confidently wrong live object:

- **No tenant directory for the tenant in question.** No workspace, recipients, vocabulary, ref
  table or registry. Do not build; run `tenant-onboard` or ask for the files.
- **No `gates.md`.** The one-line table is enough to know A2b and A7 exist, not to apply them.
  Say so before any build.

## The travelling set

| Tier | Contents | Lost if absent |
|---|---|---|
| Required | `skills/observability/SKILL.md` | Everything |
| Strongly recommended | Router `references/`, especially gates, security, run-protocol, designer-quirks | The procedures behind every gate |
| Recommended | The eight sub-skills | Build, intake, verify, health and retire procedures |
| Per tenant | `tenants/<name>/` | Everything tenant-specific: the build cannot start |
| Optional | `agents/`, `evals`, `hosts/openai.yaml`, `hooks/`, `settings.json`, `CONNECTORS.md` | Subagents, regression cases, host metadata, session reminder, defaults |

## Cross-skill references

Relative paths resolve within one skill only. Every reference across skills, to the tenants
directory or to agents uses `${CLAUDE_PLUGIN_ROOT}`. A host that flattens one skill out of the
package breaks those links; the skill must then say which file it could not open.

## Tool dependencies

The skills need a browser session (Claude in Chrome) signed in to the tenant's MoEngage workspace,
Outlook web, and Power Automate for intake work. No MCP server ships with the plugin. Without a
browser the plugin can still design, review specs, validate the registry and run the eval cases;
it cannot build, verify or audit live state, and says so.

## Validation

`python3 scripts/validate_skill.py` checks the package structure, tenant purity and secrets;
`python3 scripts/validate_registry.py tenants/<name>/alert-registry.csv` checks a registry. Neither
needs a third-party dependency. The evals are run by the `eval-runner` agent.
