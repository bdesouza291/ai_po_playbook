---
name: release
description: "Release stage. Builds a phased rollout, go/no-go checklist, monitoring and rollback plan, for PO sign-off."
argument-hint: <slug> [feedback for a revision]
disable-model-invocation: true
---

Run the **release** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS` (the first word is the initiative slug; anything after it is the PO's feedback, pass it to the agent word for word)
- Gate check: `scripts/pdlc check <slug> release`
- Subagent: `release-planner`
- Output: `work/<slug>/09-release-plan.md`
- Template: `templates/09-release-plan.md`
- Upstream artefacts to pass: `06-backlog.md`, `07-test-scenarios.md`, `05-metrics-plan.md`
- Inputs folder: `work/<slug>/inputs/`

After the draft, always run `artefact-critic` on it (protocol step 4).

Finish by handing back for sign-off (protocol step 5). Do not start the next stage.
