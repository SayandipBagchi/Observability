---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(observability:)?sentinel-flow"'
min: 1
---
# Skill fired: save-toast-is-not-success

- [ ] The `sentinel-flow` skill was consulted for this request.
- [ ] The `delivery-verify` skill was not used instead of it.
- [ ] The response follows sentinel-flow's read-back contract rather than a generic answer.
