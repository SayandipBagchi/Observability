---
type: llm
---
# Criteria: route-watchdog

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Routes to or uses the alert-watchdog approach rather than building a new alert
- [ ] Asks which model and plan vs direct before any live change, or states the live-work gate applies
- [ ] Names a missed-burst check that replays the intake's own burst rule from the log
- [ ] Names failure catches on the intake, relay and digest flows
- [ ] Names a daily silence check (no log rows in 24 h, or an alert quiet against its own history)
- [ ] Proposes the owner as the only recipient by default
- [ ] Asks the owner to approve cadence, lookback, recipient and layers before building
- [ ] Says the watchdog is built switched off and turned on only with the owner's OK
- [ ] Does not change any alert threshold, cooldown or recipient as part of the answer
