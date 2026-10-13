---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(observability:)?delivery-verify"'
min: 1
---
# Skill fired: a6-intake-vs-inbox

- [ ] The `delivery-verify` skill was consulted for this request.
- [ ] The `alert-health` skill was not used instead of it.
- [ ] The response follows delivery-verify's A6a/A6b contract rather than a generic answer.
