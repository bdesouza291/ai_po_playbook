---
name: track
description: "Switch an initiative between the full 12-stage flow and the lite flow (brief > PRD > backlog > test > close), with a logged reason."
argument-hint: <slug> <full|lite> "<reason>"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`.

Tracks decide which stages an initiative must go through:
- **full**: every stage. Use it for anything customer-facing, regulated, measured with an experiment, or needing stakeholder comms.
- **lite**: brief > PRD > backlog > test > close (plus `/handoff`). Use it for small, low-risk changes, internal tools and spikes. In lite the PRD gates on the brief alone, so the agents work from the brief and evidence and mark missing goals or baselines `[[OPEN]]`.

1. If the track or the reason is missing, ask. Show the stages the change adds or drops: `python3 scripts/pdlc.py stages --track <new>`.
2. Run `python3 scripts/pdlc.py track <slug> <track> --by "<PO name from the team file>" --reason "<reason>"`. Claude Code will ask permission; that prompt is the PO's decision.
3. Show `python3 scripts/pdlc.py status <slug>`. If moving to **full**, point out the newly required stages and that downstream gates stay shut until they're approved. Approved artefacts are kept either way.
