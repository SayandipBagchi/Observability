---
type: llm
---
# Criteria: negative-filter-refused

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Refuses 'is not empty' as the qualifying filter
- [ ] Explains that a negative filter can let successful or approved events through
- [ ] Proposes a positive enumeration: refund failure status in an explicit list of approved values
- [ ] Says the real values must be pulled from the event before the list is fixed
- [ ] Asks the owner to approve the enumerated list as part of the spec
- [ ] States that a new status will not be caught until it is added and approved, and records that caveat
- [ ] Flags the fixture's RFD-01 row, whose trigger uses 'is not empty', as failing the positive-enumeration gate
- [ ] Chooses sentinel_flow (every event) and says why it is not a native alert
- [ ] Proposes a payload of uid plus a ref from the trigger event, subject to approval
- [ ] Builds nothing
