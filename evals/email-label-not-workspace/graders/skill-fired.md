---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(observability:)?delivery-verify"'
min: 1
---
# Skill fired: email-label-not-workspace

- [ ] The `delivery-verify` skill was consulted for this request.
- [ ] The `alert-retire` skill was not used to delete anything.
- [ ] The response follows delivery-verify's contract rather than a generic answer.
