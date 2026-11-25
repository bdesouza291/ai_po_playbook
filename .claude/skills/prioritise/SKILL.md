---
name: prioritise
description: "Prioritisation stage. Compares solution options with transparent scoring and recommends MVP slicing, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **prioritisation** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `scripts/pdlc check <slug> prioritisation`
- Subagent: `prioritisation-analyst`
- Output: `work/<slug>/03-prioritisation.md`
- Template: `templates/03-prioritisation.md`
- Upstream artefacts to pass: `02-opportunity.md`, `01-discovery.md`
- Inputs folder: `work/<slug>/inputs/`

If the PO named options they already have in mind in the feedback, tell the agent to include them alongside its own.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
