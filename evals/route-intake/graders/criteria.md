---
type: llm
---
# Criteria: route-intake

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Routes the work to the intake contract, not to the MoEngage flows
- [ ] Adds uid and ref to the Parse JSON schema as strings, with ref not required
- [ ] Says the schema edit commits only after clicking out, and to reopen and read it back
- [ ] Adds the columns to the AlertLog table before mapping, typed with direct clicks
- [ ] Maps with body('Parse_JSON')?['uid'] and ['ref'], via picker or expression with the popup open
- [ ] Verifies the mapping in Code view text, not chips
- [ ] Requires the 'Your flow is ready' banner after Save
- [ ] Says never to expand or screenshot the trigger card
- [ ] Proves it with the next real AlertLog row, reporting uid and ref as present or blank
- [ ] Says earlier rows are blank in the new columns by design
