---
name: discover
description: "Discovery stage. Synthesises the evidence in an initiative inputs folder into graded findings, JTBD and pain points, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **discovery** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `python3 scripts/pdlc.py check <slug> discovery`
- Subagent: `discovery-researcher`
- Output: `work/<slug>/01-discovery.md`
- Template: `templates/01-discovery.md`
- Upstream artefacts to pass: `00-brief.md`
- Inputs folder: `work/<slug>/inputs/`

Before delegating, list the files in `inputs/`. If it only has the README, stop and ask the PO to add evidence first (interview notes, ticket extracts, reviews, analytics exports). Discovery with no evidence is guesswork.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
