# Example: replacing a flow whose name did not persist

A worked change report for a sentinel-flow replacement. IDs, times and values are invented; the
shape is what matters. The real evidence behind this pattern is in the tenant's
`quirk-evidence.md` under Q3.

Model: Opus · Mode: direct · Workspace: `<header>` (Live)

| Alert ID | Action | Object name | MoEngage ID | A0 | A1 | A2 | A2b | A3 | A4 | A5 | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XXX-07 | replace | MON XXX-07 payment mandate failed v2 | 000000000000000000000b02 | ✔ 10:02 "ok build XXX-07 v2, uid + ref mandate id" | ✔ header + Live | ✔ action values pulled | ✔ `in [<value a>, <value b>, <value c>]` | ✔ name in breadcrumb; body alertId, journey, uid, ref read via JS from Body type | ✔ Active | ✔ registry + build log 10:31 | original saved as "Duplicate - MON XXX-06…" (Q3) |

Replaced/paused chain: 000000000000000000000b01 → 000000000000000000000b02 (name did not persist; live flows cannot be renamed); registry `replaced_ids` now `000000000000000000000b01 (PAUSED, wrong name)`
Intake (A6a): NOT CHECKED (no qualifying event yet); check at next row for XXX-07
Inbox (A6b): proven for this build type on this tenant (see revisions); not re-proven for this object
Shadow check (A7): scheduled for go-live + 24 h against baseline 0.5/d
Polluted rows: none (replacement was cosmetic; the original's rows are kept and annotated)
Security: no exposure; drawer closed before every screenshot
Open items added: none
