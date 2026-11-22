---
name: ask-agent
description: "Use any PO agent for a one-off task outside the stage flow, e.g. split one story, draft a stakeholder email, size an idea."
argument-hint: <agent-name> <slug or _adhoc> <request>
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

1. Pick the agent named (or the best fit from `.claude/agents/` if none is named; say which you picked).
2. Output path: `work/<slug>/adhoc/<yyyy-mm-dd>-<short-name>.md`, or `work/_adhoc/...` if no initiative. Create the folder if needed.
3. Tell the agent this is ad-hoc: front matter with `stage: adhoc` and `status: DRAFT`, same writing and evidence rules.
4. Show the PO the result summary and path. Ad-hoc drafts can be approved with `/approve` like anything else.
