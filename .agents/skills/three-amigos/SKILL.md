---
name: three-amigos
description: "Run a structured Three Amigos deep-dive on one story or requirement — PO intent, developer feasibility, QA testability — producing sharpened acceptance criteria, risks and open questions."
argument-hint: <slug> <story-or-requirement-id>
---

Delegate to the `three-amigos-facilitator` subagent.

From `$ARGUMENTS`, take the initiative slug and the target story or requirement ID. Pass the subagent: the target ID, the relevant artefacts (`06-backlog.md` and/or `04-prd.md`), the `context/` files, and the output path `work/<slug>/adhoc/three-amigos-<id>.md`.

This is a focused, ad-hoc deep-dive — it writes a DRAFT note, it does not run the `/refine` stage or change sign-off. Show the PO the verdict (ready / split / blocked), the top risks and the open questions, and the file path. If the output should feed the refinement pack, suggest running `/refine <slug>` next.
