---
name: handover
description: "Create a concise session handover for an initiative, including objective, verified state, open decisions and the next action."
argument-hint: "<slug>"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

1. Use the first argument as the initiative slug.
2. Run `python3 scripts/pdlc.py status <slug>`.
3. Read the initiative artefacts, approvals log and any relevant input files.
4. Write `work/<slug>/handover.md` with:
   - objective
   - verified facts and evidence
   - artefacts approved or in draft
   - stale or changed artefacts
   - open decisions
   - unresolved risks
   - the one next concrete action
5. State only what is supported by files or command output. Do not copy secrets into the handover.
6. Show the PO the handover location and the next action.
