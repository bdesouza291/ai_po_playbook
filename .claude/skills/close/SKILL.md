---
name: close
description: "Close-out stage. Checks delivered tests and results against the PRD's requirement and scenario IDs, finds drift and drafts follow-ups, for PO sign-off."
argument-hint: <slug> <evidence path(s)> [feedback for a revision]
disable-model-invocation: true
---

Run the **close** stage following the *Stage run protocol* in CLAUDE.md.

- Arguments: `$ARGUMENTS`. The first word is the slug. Then come the evidence paths: test result files (JUnit XML is best), test folders or feature files, typically from the product repo or a CI export. Anything after them is the PO's feedback.
- If no evidence path is given, ask for one. Explain that results files (JUnit XML from CI) give pass and fail status; test source folders only show that a test *exists*.
- **Gate check:** `python3 scripts/pdlc.py check <slug> close`
- **Delivery evidence:** `python3 scripts/pdlc.py trace <slug> --evidence <paths>`. Pass its full output to the agent as the source of truth.
- Subagent: `close-analyst`
- Output: `work/<slug>/12-close-report.md`
- Template: `templates/12-close-report.md`
- Upstream artefacts to pass: those on the gate's `UPSTREAM:` line, plus `04-prd.md`, any `handoff/*.md` build specs, and the `inputs/` folder (PR build logs, release notes, defects, ops feedback)

After the draft, offer `artefact-critic`, then hand back for sign-off (protocol step 5). Lead with the verdict, the Must gaps and the drift items that need a PRD `/reopen`. Follow-up stories in the report are drafts: they reach the backlog only through `/reopen` and `/stories`.
