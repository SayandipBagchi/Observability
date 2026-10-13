# Alert registry schema

Author: Sayandip Bagchi.

`tenants/<name>/alert-registry.csv`, UTF-8, one row per alert ID, holding the **currently live**
MoEngage object. Every predecessor it replaced is in `replaced_ids`. The header row is in
`${CLAUDE_PLUGIN_ROOT}/tenants/_template/alert-registry.csv`.

| Column | Meaning | Allowed |
|---|---|---|
| `alert_id` | Stable ID; suffix a/b for a split native alert | `^[A-Z]{3}-[A-Z]?\d{1,2}[a-z]?$` (placeholder in docs: `XXX-01`) |
| `prd_ref` | Row ID in the source observability sheet, or `(added after sheet)` for alerts added after the sheet | |
| `module`, `kpi`, `severity` | From the sheet | severity: `P1`, `P2`, `P3`, `Build ask`, blank |
| `build_type` | See `mechanisms.md` | `native_alert`, `sentinel_flow`, `system_alert_subscription`, `out_of_moengage` |
| `trigger` | The rule as built (flows) or as specified (others), filters written out | Live sentinel flows: positive enumeration only (A2b) |
| `threshold_decision` | The owner's decision column, verbatim | |
| `baseline` | Events per day with its window, for example `12.0/d (4–25) · <from>–<to>` | Required for A7 |
| `cadence_or_wait` | Native: evaluation cadence. Flow: wait window or `every event` | Flow wait ≥ 5 min |
| `journey` | The connector `journey` value | One of the tenant's journeys |
| `moengage_name`, `moengage_id` | The live object's exact name and ID | Live flows need a 24-hex ID |
| `replaced_ids` | **The full chain** of predecessors, oldest first, `;`-separated, each entry a 24-hex ID with an optional `(reason)` | Every entry carries a 24-hex ID |
| `build_status` | | `live`, `paused`, `not_built`, `build_ask`, `retired`, `unverified` |
| `verified_on`, `verified_how` | Date and method of the last check; the source if not checked in-session | Required for live, retired, unverified |
| `acquisition_dependent` | Fires only while new applications flow | `yes`, `yes (proposed)`, `yes (confirmed <date>)`, blank |
| `notes` | Decisions, caveats, the payload decision, `exclusion-approved:` waivers | No email address, no URL |

---

## The replace chain

A flow can be replaced more than once in a day (v1 → v2 → v3). `replaced_ids` keeps **every**
predecessor, not just the last, oldest first:

```
<v1 id> (PAUSED, <reason>);<v2 id>
```

`moengage_id` holds only the live object. Dropping a middle link loses the only record that the
middle version wrote rows to the intake log, which is what the polluted-row cleanup needs.

## The payload decision: `ref` may be blank, with a reason

Every live sentinel flow's `notes` records its payload:

- `payload: uid + ref=MOE_TRIGGER_EVENT.<event>.<attribute>`, or
- `payload: uid (no ref)` with the reason either inline or in `tenants/<name>/ref-table.md`.

`ref` is blank by design when the trigger event carries no stable identifier, or when the only
identifier is session-scoped (session IDs are not in the personalisation picker). A blank `ref`
with no recorded reason is a finding.

### Stored notation vs live token

The registry, the ref table and build logs store the ref path in **ASCII dotted notation**:
`MOE_TRIGGER_EVENT.<event>.<attribute>`. That is a storage convention only. **The live token in
the connector body uses U+2024 (ONE DOT LEADER, `․`) as the separator**, not a full stop:

```
stored:  MOE_TRIGGER_EVENT.<event>.<attribute>
live:    {{EventAttribute['MOE_TRIGGER_EVENT․<event>․<attribute>']}}
```

Convert when building; never paste the stored form into the connector. The validator refuses a
U+2024 character in the registry so the two forms cannot be mixed.

## Exclusion waivers

A live sentinel flow whose trigger contains `!=`, `not in` or `is not empty` fails validation
unless `notes` carries `exclusion-approved:` stating the positive anchor it narrows and the
decision that approved it (A2b).

---

`scripts/validate_registry.py` enforces: required columns; unique IDs; allowed enums; a 24-hex
`moengage_id` and a journey on every live flow; a name on every live object; verification fields;
24-hex IDs in every `replaced_ids` entry; positive enumeration on live flow triggers (with the
waiver); a payload decision in `notes` for every live flow; no U+2024 in stored refs; and no URL,
signature parameter or email address in any cell.
