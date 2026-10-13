---
type: llm
---
# Criteria: ref-token-separator

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Identifies the separator: the dots in the ref path must be U+2024 (one dot leader), not full stops
- [ ] Says a full-stop version saves and reads back plausibly but resolves blank
- [ ] Says the flow is live, so the fix is a replacement, not an edit
- [ ] Recommends inserting the token via the personalisation picker or pasting the U+2024 form
- [ ] Recommends verifying the code point in the JS read-back rather than by eye
- [ ] Checks that the ref attribute belongs to the trigger event, since only trigger-event attributes are personalisable
- [ ] Says the next intake row after the replacement should show Ref present (A6a)
- [ ] Notes the registry stores the dotted ASCII form and it must be converted when building
- [ ] Reports resolved values as present or blank only, never quoting a uid or ref value
