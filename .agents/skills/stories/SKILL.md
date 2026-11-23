---
name: stories
description: "Backlog stage. Breaks the approved PRD into epics and INVEST user stories with Gherkin acceptance criteria, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **backlog** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `python3 scripts/pdlc.py check <slug> backlog`
- Subagent: `story-writer`
- Output: `work/<slug>/06-backlog.md`
- Template: `templates/06-backlog.md`
- Upstream artefacts to pass: `04-prd.md`, `05-metrics-plan.md`
- Inputs folder: `work/<slug>/inputs/`

After the draft, always run `artefact-critic` on it. Then show the PO the story count per epic and any PRD requirement with no story.

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
