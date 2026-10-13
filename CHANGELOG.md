# Changelog — observability

## 1.0.0

First public release.

- Router skill `observability` with the model gate, gates A0–A7 and the security rules.
- Nine job skills: `alert-design`, `native-alert`, `sentinel-flow`, `alert-intake`,
  `delivery-verify`, `alert-health`, `alert-retire`, `alert-watchdog`, `tenant-onboard`.
- Eight subagents (builders, reviewers, auditor, shadow triangulator, eval runner).
- 23 eval cases with graders and two invented fixtures.
- `tenants/_template/` plus a fully fictional example tenant showing every file filled in.
- Validators (`validate_skill.py`, `validate_registry.py`) with config-driven tenant guards.
- `scripts/leak_scan.py` and a `.githooks/pre-commit` hook that block private terms, secrets and
  non-example email domains before a commit.
