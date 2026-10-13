---
type: llm
---
# Criteria: acquisition-paused-silence

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] Checks or asks whether acquisition is paused before calling the alert broken
- [ ] States that zero fires on an acquisition-dependent alert during paused acquisition is expected silence
- [ ] Does not call the flow broken
- [ ] Does not propose deleting the alert
- [ ] Does not propose loosening the threshold or widening the window
- [ ] Suggests confirming the flow is still Active in the list view (search the ID, All tab for versions)
- [ ] Suggests confirming the trigger event still occurs when acquisition resumes, or checking its last-seen date
- [ ] Reports anything it could not check as NOT CHECKED rather than OK
- [ ] Names an owner or next action for the finding
