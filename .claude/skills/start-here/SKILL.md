---
name: start-here
description: "Entry point for a new or returning session. Inspect repository state and recommend the next Product Owner action."
argument-hint: "[slug or situation]"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

1. Run `scripts/pdlc status` and `scripts/pdlc context-check`.
2. If the argument names an initiative, run `scripts/pdlc status <slug>`.
3. Check for:
   - unfinished context setup
   - drafts waiting for sign-off
   - stale or changed approved artefacts
   - blocked upstream gates
   - the next command named by `/next`
4. Explain the current state in five lines or fewer.
5. Recommend one next action and ask whether to run it. Do not approve, reopen or override without an explicit human invocation.
