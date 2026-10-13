---
type: llm
---
# Criteria: save-toast-is-not-success

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] States that a Save toast is not evidence the flow persisted
- [ ] Requires closing and reopening the flow before any read-back
- [ ] Requires read-back of trigger, filters, wait, name, alertId and journey against the spec (A3)
- [ ] Requires the connector body to be read via JS rather than a screenshot
- [ ] Checks that the ref token separator is U+2024 if the flow carries a ref
- [ ] Requires the flow to show Active in the list view before it is called live (A4)
- [ ] Does not mark the registry row live in this response
- [ ] Says the registry and build log are updated for this flow once A3 and A4 pass, before moving to the next flow
- [ ] Mentions the one-field-per-save-pass quirk as a reason a key may not have persisted
