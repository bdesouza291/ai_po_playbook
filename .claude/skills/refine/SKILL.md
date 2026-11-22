---
name: refine
description: "Refinement stage. Prepares a refinement session pack with agenda, questions, risks and split options, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **refinement** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `python3 scripts/pdlc.py check <slug> refinement`
- Subagent: `refinement-facilitator`
- Output: `work/<slug>/08-refinement-pack.md`
- Template: `templates/08-refinement-pack.md`
- Upstream artefacts to pass: `06-backlog.md`, `07-test-scenarios.md`
- Inputs folder: `work/<slug>/inputs/`

If the PO pasted notes from a finished session as feedback, tell the agent to add a "Proposed backlog changes" section rather than editing the backlog.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
