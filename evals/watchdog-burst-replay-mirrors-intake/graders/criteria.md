---
type: llm
---
# Criteria: watchdog-burst-replay-mirrors-intake

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Says to read the intake's burst condition in Code view before writing the check
- [ ] Uses a 'meets or exceeds' comparison, not equality
- [ ] Accounts for the current event possibly missing from a list made straight after the add (count older rows plus one)
- [ ] Uses a lookback that tiles consecutive runs without overlap
- [ ] Excludes rows already covered by last-fired plus cooldown
- [ ] Replaces createArray() with an empty-array form that works at run time
- [ ] Divides a float, not two integers, when converting ticks to days
- [ ] Builds the flow switched off and reads every action back in Code view
- [ ] Asks for owner approval of cadence and recipient before building
