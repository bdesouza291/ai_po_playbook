---
name: handoff
description: "Write a self-contained build spec for one approved story, ready for a developer or an AI coding agent to implement. For PO sign-off."
argument-hint: <slug> <story-id> [feedback for a revision]
disable-model-invocation: true
---

Write the build spec for one story, following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS`. The first word is the slug, the second is the story ID (as in `06-backlog.md`, e.g. `EU1-S3`). Anything after that is the PO's feedback; pass it to the agent word for word.
- If no story ID is given, run `python3 scripts/pdlc.py status <slug>`, show which stories have no build spec yet, and ask which one.
- **Gate check:** `python3 scripts/pdlc.py check <slug> handoff --story <story-id>`
- **Verbatim extract:** `python3 scripts/pdlc.py story <slug> <story-id>`. Pass its full output to the agent. It is the source for the spec's story, requirement and acceptance sections, and must not be paraphrased.
- Subagent: `build-spec-writer`
- Output: `work/<slug>/handoff/<story-id>.md`
- Template: `templates/handoff-spec.md`
- Upstream artefacts to pass: those listed on the gate's `UPSTREAM:` line, plus `04-prd.md`

After the draft:
1. Run `python3 scripts/pdlc.py trace <slug>` and check for warnings about this build spec (missing or foreign scenario tags). If there are any, re-run the agent with them as feedback before showing the PO.
2. Offer `artefact-critic` (it has a build-spec rubric).
3. Hand back for sign-off (protocol step 5). Highlight the `[[TECH LEAD]]` gaps and any blocking open questions: the tech lead fills those in before the spec goes to an AI agent.

One story per run. To do several, run `/handoff` again for the next story.
