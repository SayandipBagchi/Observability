---
type: llm
---
# Criteria: route-native-vs-flow

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Assigns (a) to a native alert (Events Volume, decrease vs previous 7 days)
- [ ] Assigns (b) to a sentinel flow: screen event, then NO completion event within 20 minutes
- [ ] Explains the rule: aggregate rate or volume goes native; per-user journey break goes to a flow
- [ ] Notes the flow's wait is at least the 5-minute minimum
- [ ] Notes a flow has no threshold inside MoEngage and every qualifying trip posts
- [ ] Asks for or states the baseline with its window for each
- [ ] Proposes a payload for (b) (uid, and a ref from the trigger event or uid only) for approval
- [ ] Does not build either alert
- [ ] Ends with an approval request or table for both
