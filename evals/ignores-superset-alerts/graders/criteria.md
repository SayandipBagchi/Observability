---
type: llm
---
# Criteria: ignores-superset-alerts

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Does not build or propose a MoEngage native alert or sentinel flow for this
- [ ] Does not run the MoEngage model gate or ask plan vs direct for MoEngage work
- [ ] Does not ask for a MoEngage workspace, tenant folder or alert registry row
- [ ] Addresses the request as a Superset or warehouse alert
- [ ] Contains none of: sentinel flow, connector body, AlertLog, Power Automate intake
- [ ] Does not quote any gate named A0 to A7
- [ ] Does not mention the intake signature
- [ ] Answers or routes the actual question rather than refusing outright
