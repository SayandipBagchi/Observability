---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(observability:)?(alert-watchdog|delivery-verify)"'
min: 1
---
# Skill fired: watchdog-silence-is-not-delivery

- [ ] The `alert-watchdog` or `delivery-verify` skill was consulted for this request.
- [ ] The response follows alert-watchdog's contract rather than a generic answer.
