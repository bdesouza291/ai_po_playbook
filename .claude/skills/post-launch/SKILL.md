---
name: post-launch
description: "Post-launch stage. Reviews results against targets and recommends scale, iterate, roll back or stop, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **postlaunch** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `scripts/pdlc check <slug> postlaunch`
- Subagent: `metrics-analyst`
- Output: `work/<slug>/11-post-launch-review.md`
- Template: `templates/11-post-launch-review.md`
- Upstream artefacts to pass: `05-metrics-plan.md`, `09-release-plan.md`, `04-prd.md`
- Inputs folder: `work/<slug>/inputs/`

Tell the agent it is in **review mode**. Check `inputs/` has results data first; if not, ask the PO for it.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
