---
name: next
description: "Work out the next PDLC step for an initiative and offer to run it."
argument-hint: <slug>
disable-model-invocation: true
---

1. Run `python3 scripts/pdlc.py status $ARGUMENTS`.
2. Read the "Next:" line.
   - If a DRAFT is waiting for sign-off, summarise it in three lines (read the file) and ask: approve, revise, or critique first?
   - If a stage is ready to run, name the command and ask the PO whether to run it now.
   - If anything is STALE or CHANGED SINCE APPROVAL, raise that first.
3. Wait for the PO's answer. Don't run anything that changes status yourself.
