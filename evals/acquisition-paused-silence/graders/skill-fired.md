---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(observability:)?alert-health"'
min: 1
---
# Skill fired: acquisition-paused-silence

- [ ] The `alert-health` skill was consulted for this request.
- [ ] The `alert-retire` skill was not used to delete or pause anything.
- [ ] The response follows alert-health's finding format rather than a generic answer.
