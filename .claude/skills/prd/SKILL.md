---
name: prd
description: "PRD stage. Writes the product requirements document or spec from the approved opportunity and prioritisation, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **prd** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `python3 scripts/pdlc.py check <slug> prd`
- Subagent: `prd-writer`
- Output: `work/<slug>/04-prd.md`
- Template: `templates/04-prd.md`
- Upstream artefacts to pass: `02-opportunity.md`, `03-prioritisation.md`, `01-discovery.md`
- Inputs folder: `work/<slug>/inputs/`

After the draft, always run `artefact-critic` on it (protocol step 4).

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
