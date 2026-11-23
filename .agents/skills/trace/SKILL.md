---
name: trace
description: "Check traceability across the PRD, backlog and test scenarios: which requirements have stories and tests, what's a gap, and any orphaned ID references."
argument-hint: <slug> [--deep]
---

Check the requirement → story → test chain for initiative `$ARGUMENTS`.

1. **Code-based check first (always).** Run `python3 scripts/pdlc.py trace <slug>` (or `python ...` on Windows). It parses the stable IDs and reports coverage per requirement, gaps, orphaned IDs, PRD scenarios with no test, and area-code clashes with other initiatives. This is the source of truth for coverage. Don't recount it yourself.
2. Show the PO the verdict and any gaps or warnings, briefly. If there are gaps in Must or Should requirements, suggest the fix: `/stories <slug>` to add stories, `/test-scenarios <slug>` to add scenarios. Remind them that the release gate blocks while a Must requirement has no story or test scenario.
3. **Qualitative review (only with `--deep`, or if the PO asks).** Delegate to the `traceability-report` subagent with the PRD, backlog and test-scenario paths and the script's output. Ask it to judge what the script can't: whether a story *really* delivers the requirement it claims, and whether a test scenario *really* exercises its requirement.

Do not change any artefact.
