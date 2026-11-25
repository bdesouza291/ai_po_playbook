---
name: setup-check
description: "Check the kit works on this machine: Python, the ledger script, the sign-off guard hook (Bash and PowerShell), the permission prompt and the context files."
---

Run these checks and report a short pass / fail table.

1. **Python.** Run `python3 --version`. If it fails, try `python --version`. Note which one works. The hook falls back to `python`, and the `scripts/pdlc` wrapper (`scripts/pdlc.cmd` in PowerShell) picks whichever works, so either is fine; if neither works, that is the failure to report.
2. **Ledger.** Run `scripts/pdlc stages` (in PowerShell: `scripts/pdlc.cmd stages`). This also proves the wrapper finds Python.
3. **Status.** Run `scripts/pdlc status`. The worked example's stages 00–11 should be APPROVED. The refinement pack is flagged STALE on purpose (the backlog changed after the session). If `close` and the `EU1-S3` build spec show DRAFT, the PO hasn't signed off those example additions yet. That's not a failure; mention it.
4. **Guard logic.** Run `python3 scripts/test_guard.py`. Expected: every case passes. It simulates Write/Edit, Bash and PowerShell calls against the approved example files without changing anything.
4b. **Ledger logic.** Run `python3 scripts/test_pdlc.py`. Expected: every case passes. It tests tracks, gates, build specs, traceability and delivery evidence in a temporary copy, without touching `work/` or `examples/`.
5. **Guard is live (file tools).** Try to append a line `test` to `examples/flexpay-early-upgrade/04-prd.md` with the Edit tool. Expected: **blocked** by the PO sign-off guard. If it succeeds, the hook isn't running: undo the change immediately and tell the PO to check `.claude/settings.json` hooks, that Python is on PATH, and that this folder (not a parent folder) is open as the project.
6. **Guard is live (shell).** If a PowerShell tool is available (Windows), run `Add-Content examples/flexpay-early-upgrade/04-prd.md "test"` with it. Otherwise run `echo test >> examples/flexpay-early-upgrade/04-prd.md` with Bash. Expected: **blocked**. If it ran, remove exactly the line you added, confirm `pdlc.py status` shows no `CHANGED SINCE APPROVAL`, and report the failure.
7. **No self-approval.** Try to Write `work/_setup-test.md` containing front matter with `status: APPROVED`. Expected: **blocked**. If it was written, delete it and report the failure.
8. **Traceability.** Run `scripts/pdlc trace flexpay-early-upgrade`. Expected verdict: READY.
9. **Context.** Run `scripts/pdlc context-check`. In a fresh copy of the template the REQUIRED files will show placeholders. That isn't a failure, but tell the PO to run `/onboard` before starting real work.
10. **Permission prompt.** Explain that the first time `/approve` runs, Claude Code should ask permission for `scripts/pdlc approve`. Also run `python3 scripts/pdlc.py context-check` or read `context/team-and-ways-of-working.md`: the signer comes from the Product Owner named there, and `/approve` stops until it is filled in. If it doesn't ask, check the PO isn't in bypass-permissions mode.
11. **Template validator.** Run `python3 scripts/validate_template.py`. Expected: every skill mirror, release evidence fields and Python file parses. This is the cross-agent and CI structure check.

End with one line: ready, or what to fix.
