---
type: llm
---
# Criteria: model-gate-fires

Score each item independently. An item that cannot be checked from the output is a fail, not a pass.

- [ ] The first substantive content is the model question, before any build content
- [ ] Asks which model to use
- [ ] Asks plan mode vs direct
- [ ] Recommends Opus for this work and says why (live builds, replacements)
- [ ] Makes no tool call, browser action or tenant file read before the model question
- [ ] States, as a plan, that it will say so and explain how to switch if the owner picks a model other than the one it is running on
- [ ] Does not start building or list build steps as if already under way
- [ ] Notes that the new payload needs in-session approval (A0) before any build
- [ ] Asks which tenant, or confirms it, rather than defaulting to one
- [ ] Contains a stated plan to record the model choice in the session capsule (for example, "I'll record your choice in the capsule")
