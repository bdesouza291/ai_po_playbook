---
name: test-scenarios
description: "Test stage. Designs happy, negative, edge, accessibility and analytics test scenarios from approved stories, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **test** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `scripts/pdlc check <slug> test`
- Subagent: `qa-scenario-designer`
- Output: `work/<slug>/07-test-scenarios.md`
- Template: `templates/07-test-scenarios.md`
- Upstream artefacts to pass: `06-backlog.md`, `04-prd.md`
- Inputs folder: `work/<slug>/inputs/`

When handing back, list the acceptance-criteria gaps the agent found. The PO may want to /reopen the backlog to fix them.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
