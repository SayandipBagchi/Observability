---
type: llm
---
# Criteria: tenant-purity-no-carryover

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Refuses to copy the Aurora folder and edit it
- [ ] Starts from tenants/_template/ instead
- [ ] Does not carry Aurora event names across as the new programme's
- [ ] Does not carry Aurora alert IDs, names or MoEngage IDs across
- [ ] Does not carry Aurora recipients across; asks for the new programme's recipients
- [ ] Asks for the new workspace header, email label, host and environment
- [ ] Says the event vocabulary must be proven on the new workspace, even with the same codebase
- [ ] Asks for the intake name and owner, and says the URL is never stored
- [ ] Seeds the new registry with every row not_built and the ref table unapproved
- [ ] Says no code edits are needed, only the tenant folder
- [ ] Quotes no Aurora baseline or fire count as applying to the new programme
