---
name: critique
description: "Get an independent, rubric-based review of any draft artefact before signing it off."
argument-hint: <path to artefact>
---

Delegate to the `artefact-critic` subagent with the artefact path `$ARGUMENTS`, its upstream artefacts (from its `upstream` front matter), and the initiative's `inputs/` folder.
Show the PO the verdict, the top three issues and the review file path. Ask whether they want the drafting agent to address the issues (re-run the stage command with the critic's points as feedback).
