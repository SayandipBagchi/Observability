# Context engineering: what to hold open during live UI work

Author: Sayandip Bagchi.

Alert builds are long browser sessions: a dozen flows, each opened, edited, saved, reopened and
read back, with screenshots in between. Screenshots are the most expensive thing in context, and
they evict the spec you approved. That is a correctness problem, not a cost problem: **the failure
mode is building flow eleven against a spec you now remember rather than one you can read.**

---

## The loading budget

1. **The router `SKILL.md` is always in context.** It carries the gates and the routing table.
2. **One sub-skill per task.** A build is `sentinel-flow` *or* `native-alert`; intake mapping is
   `alert-intake`. A request spanning two is two sequential tasks with a handover.
3. **At most two reference files open.** Typically the owning skill's reference plus
   `designer-quirks.md`.
4. **One tenant file section at a time.** The registry rows being built, the ref-table rows for
   those alerts, and `config.json`. Not `revisions.md`, not the whole `journeys.md`.

## Per-task load table

| Task | Permitted | Not open |
|---|---|---|
| Design | `alert-design` + its references; registry rows in scope; the source sheet rows | Build references, intake references |
| Flow build / replace | `sentinel-flow` + `designer-quirks.md`; registry + ref-table rows in scope; `config.json` | Intake and sheet-sync references |
| Native build | `native-alert` + its reference; registry rows; `config.json` recipients | Flow references |
| Intake mapping | `alert-intake` + one of its references | MoEngage build references |
| Verify | `delivery-verify`; registry row; `revisions.md` A6 lines | Build references |
| Health / shadow | `alert-health`; the full registry; intake log counts | Build references |

## Screenshots

- Take a screenshot to decide the next click, then **stop carrying it**: write down what it showed
  (one line) and let it go.
- Never screenshot to prove a value that JS can read; JS output is smaller and exact.
- Re-screenshot before every coordinate click (`designer-quirks.md` Q20). An old frame is both
  stale and in the wrong coordinate space.

## Eviction and re-read

- **Re-read the approved spec row before each object**, not once per session. The approval quote
  goes into the change report line for that object as it is built.
- After 7–8 prompts of UI work, offer a new session (`run-protocol.md`, *Session hygiene*).
- If you notice you are unsure which version (v2 or v3) of a flow you are on, stop and read the
  list view by ID before any further click.

## The capsule as handover

Every session ends with [the capsule template](../templates/context-capsule.md): what was built with IDs, gates passed and
NOT CHECKED, open items with owners, security notes, next action. The next session starts by
reading the capsule and the registry, never by recalling.
