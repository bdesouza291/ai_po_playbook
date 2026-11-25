---
name: frame
description: "Opportunity stage. Frames the problem, outcome, sizing, hypotheses and riskiest-assumption tests, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **opportunity** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `scripts/pdlc check <slug> opportunity`
- Subagent: `opportunity-framer`
- Output: `work/<slug>/02-opportunity.md`
- Template: `templates/02-opportunity.md`
- Upstream artefacts to pass: `01-discovery.md`, `00-brief.md`
- Inputs folder: `work/<slug>/inputs/`

Remind the agent to show all sizing arithmetic with low / likely / high and to label every input Known or Assumed.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
