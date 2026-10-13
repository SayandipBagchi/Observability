---
type: llm
---
# Criteria: watchdog-turn-on-gate

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Applies the live-work gate (model and mode) or confirms it was answered, before switching on
- [ ] Requires a clean flow checker and a read-back from the saved state before switching on
- [ ] Asks for the owner's explicit OK to switch it on
- [ ] Says the first scheduled run must be verified before calling it live
- [ ] Reports each layer as proven, not proven or not checked
- [ ] Explains the platform's weekly failure summary is not a watchdog email
- [ ] Says to check run-history dates because the summary lists already-fixed failures
- [ ] Records the flow ID, cadence and recipient in the tenant config and revisions
