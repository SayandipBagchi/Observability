---
type: llm
---
# Criteria: excel-namebox-race

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Warns that typed text can land in the Name box or Copilot pane instead of the cell
- [ ] Says to click each target cell and confirm the address in the Name box before typing
- [ ] Says not to use Tab inside the table because it wraps to the next row
- [ ] Says the screen is not verification
- [ ] Says the downloaded saved copy is the only valid verification and can lag by minutes
- [ ] Proposes a baseline snapshot before the batch and a diff after it
- [ ] Says any unexpected changed cell is reported with its address and restored
- [ ] Does not declare the task done on the basis of the screen
- [ ] Says the change is recorded only after the saved copy verifies
