---
name: reopen
description: "Reopen an APPROVED artefact as a new DRAFT version, with a reason, so it can be revised."
argument-hint: <path to artefact> "<reason>"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS` (path, then the reason).

1. If no reason was given, ask for one. The reason goes in the approvals log.
2. Run `scripts/pdlc reopen <path> --reason "<reason>"` (Claude Code will ask permission). Do not pass `--by`; the script records the PO named in the team file.
3. Show `scripts/pdlc status <slug>` and point out any downstream artefacts now flagged, as they may need revisiting too.
