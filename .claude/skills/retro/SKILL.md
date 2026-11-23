---
name: retro
description: "Turn a session failure or repeated issue into an instruction, hook or test change, or conclude that no setup change is warranted."
argument-hint: "[scope or failure]"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

1. Establish what happened, what evidence showed the failure, and whether it was isolated or repeated.
2. Check `CLAUDE.md`, `AGENTS.md`, relevant skills, hooks and scripts for the controlling rule.
3. Recommend the smallest durable fix: an instruction, hook, template, script or test.
4. Show the proposed change and ask the PO to confirm it before editing repository setup.
5. Make the change, run the smallest covering validation, and record the outcome in a session handover or a changelog entry only if the project convention requires it.
6. Do not rewrite source artefacts or approvals to fit the lesson.
