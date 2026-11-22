---
name: reopen
description: "Reopen an APPROVED artefact as a new DRAFT version, with a reason, so it can be revised."
argument-hint: <path to artefact> "<reason>"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS` (path, then the reason).

1. If no reason was given, ask for one. The reason goes in the approvals log.
2. Get the PO's name from `context/team-and-ways-of-working.md`.
3. Run `python3 scripts/pdlc.py reopen <path> --by "<PO name>" --reason "<reason>"` (Claude Code will ask permission).
4. Show `python3 scripts/pdlc.py status <slug>` and point out any downstream artefacts now flagged, as they may need revisiting too.
