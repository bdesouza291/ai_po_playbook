---
name: meeting
description: "Turn pasted meeting notes or a transcript into decisions, actions, risks and proposed changes for an initiative."
argument-hint: <slug> [topic] then paste the notes
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

1. If the notes aren't in the message, ask the PO to paste them or name a file in `inputs/`.
2. Delegate to `meeting-scribe` with the slug, the notes, today's date, the topic, and the paths of the initiative's current artefacts.
3. Show the PO: decisions (flag any marked Unconfirmed), actions without owners, and the proposed changes.
4. Ask which proposed changes they want applied. For APPROVED artefacts, that means `/reopen` first; for DRAFTs, re-run the stage command with the changes as feedback.
