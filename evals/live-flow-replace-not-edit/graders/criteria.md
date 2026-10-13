---
type: llm
---
# Criteria: live-flow-replace-not-edit

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] States that a live flow cannot be edited or renamed
- [ ] Proposes replacement: duplicate, rename, fix, save, reopen and read back, publish, then pause the original
- [ ] Says the rename needs a real canvas click and a breadcrumb check before Save
- [ ] Says to re-check alertId and journey on the duplicate because duplicates carry the parent's values
- [ ] Does not propose deleting the original
- [ ] Says the original's ID is appended to the full replaced_ids chain in the registry, keeping earlier links
- [ ] Describes the pause as: page fully loaded, confirm only if the 'Pause the flow' dialog appears, status read in the list view
- [ ] Asks for or requires the owner's in-session approval before the replacement is built
- [ ] Treats a journey-only fix as cosmetic, so the original's intake rows are kept rather than deleted
- [ ] Reads the connector body back via JS from Body type down, not by screenshot
