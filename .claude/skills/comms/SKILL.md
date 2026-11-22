---
name: comms
description: "Comms stage. Writes stakeholder, internal, customer and support communications for the release, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **comms** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `python3 scripts/pdlc.py check <slug> comms`
- Subagent: `stakeholder-comms`
- Output: `work/<slug>/10-comms.md`
- Template: `templates/10-comms.md`
- Upstream artefacts to pass: `09-release-plan.md`, `04-prd.md`
- Inputs folder: `work/<slug>/inputs/`

If the feedback names a specific audience, tell the agent to focus there but still fill the other sections briefly.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
