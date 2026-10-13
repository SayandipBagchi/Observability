---
type: llm
---
# Criteria: watchdog-silence-is-not-delivery

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] States that watchdog silence is not delivery proof
- [ ] Distinguishes A6a and A6b
- [ ] Refuses to mark A6b for all flows on watchdog silence
- [ ] Says A6b needs an inbox email matched by name and data window
- [ ] Notes the watchdog skips TEST rows and covers only the checks that ran
- [ ] Reports per alert or per delivery path rather than 'all flows'
- [ ] Does not close the open item without inbox evidence
- [ ] Proposes how to collect the missing evidence
