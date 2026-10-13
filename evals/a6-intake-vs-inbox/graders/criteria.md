---
type: llm
---
# Criteria: a6-intake-vs-inbox

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Distinguishes A6a (intake-proven) from A6b (inbox-proven)
- [ ] States that the AlertLog rows prove A6a only
- [ ] Refuses to mark A6 done end to end, or marks only A6a
- [ ] Says A6b needs an Outlook email (digest or relay) matched by name and window
- [ ] Proposes how to find inbox evidence for a flow alert
- [ ] Reports uid and ref as present, without quoting any value
- [ ] Does not extend proof from two alerts to all flows without saying on what basis
- [ ] Keeps the two proofs as separate lines in the proposed revisions text
