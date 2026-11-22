---
name: metrics
description: "Metrics stage. Defines success metrics, tracking plan and experiment design with sample size, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **metrics** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `python3 scripts/pdlc.py check <slug> metrics`
- Subagent: `metrics-analyst`
- Output: `work/<slug>/05-metrics-plan.md`
- Template: `templates/05-metrics-plan.md`
- Upstream artefacts to pass: `04-prd.md`, `02-opportunity.md`
- Inputs folder: `work/<slug>/inputs/`

Tell the agent it is in **plan mode**.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
