---
name: override
description: "Let a stage run before its upstream artefacts are approved, with a logged reason. Use sparingly."
argument-hint: <slug> <stage> "<reason>"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

Real teams sometimes skip steps (a regulatory fix, a spike). This records that choice.
1. If no reason was given, ask for one.
2. Run `python3 scripts/pdlc.py override <slug> <stage> --by "<PO name from the team file>" --reason "<reason>"` (Claude Code will ask permission).
3. Tell the PO they can now run the stage command, and that the override is in `approvals-log.md`.
