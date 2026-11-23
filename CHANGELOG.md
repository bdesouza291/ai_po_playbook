# Changelog

Version history of this template. When you copy the template for a project, note the version you started from, so you can tell which later improvements are worth pulling in.

## Unreleased

### Added
- Light and dark lifecycle images for the README, with a reproducible Pillow generator in `assets/`.
- `/start-here` entry point for routing a new or returning session to the next Product Owner action.
- `/handover` and `/retro` skills for session continuity and durable setup improvements.
- `AGENTS.md` with repository-maintenance rules for Claude and other coding agents.
- Cross-agent skill mirror under `.agents/skills/`.
- `scripts/validate_template.py` for skill mirrors, release evidence fields and Python syntax.
- `.github/workflows/tests.yml` for template validation and the PDLC and guard regression suites.
- MIT `LICENSE.md`.
- Release-plan evidence fields for the reviewed build, independent review, intended-versus-implemented, optional deeper audits, and promotion verification.

## [1.2.0] - 2026-11-21

Closes the loop with the people and agents who build it, and stops small work paying for twelve gates.

### Added
- **Tracks.** `full` (every stage) or `lite` (brief → PRD → backlog → test → close). You choose at `/new-initiative` and switch with `/track`, which asks permission and is logged. A skipped stage's gate passes straight through. `/status` shows skipped stages, and `pdlc.py stages --track lite` prints the effective gates.
- **`/handoff <slug> <story-id>`**: a self-contained **build spec per story** for developers or AI coding agents (new `build-spec-writer` agent, `templates/handoff-spec.md`). Its requirements and acceptance criteria come verbatim from the new `pdlc.py story` extract. It has a fixed "rules for AI coding agents" block, and `[[TECH LEAD]]` gaps instead of invented technical detail. It gates on backlog, test and (full track) refinement.
- **`/close <slug> <evidence>`**: a new close stage (new `close-analyst` agent, `templates/12-close-report.md`). `pdlc.py trace --evidence` reads JUnit XML results, manual test logs (CSV with a Result column) and test folders, and scores each requirement Implemented (full / partial) or no evidence. A failing test anywhere beats a pass elsewhere. `--strict` fails while any Must isn't fully implemented.
- `pdlc.py trace` now reports build-spec coverage and **spec drift**: a spec missing its story's scenarios, or carrying scenarios for requirements the story doesn't deliver.
- `/status` lists build specs, with `STALE` and `CHANGED SINCE APPROVAL` flags.
- `scripts/test_pdlc.py`: 30 regression tests for the ledger, run by `/setup-check`.
- Rubrics for build specs and close reports in `context/quality-rubrics.md`.
- Worked example: a build spec (`handoff/EU1-S3.md`), delivery evidence in `inputs/` (CI results, a manual test log, PR build logs), and a close report (`12-close-report.md`). These two artefacts are **left as DRAFT** for the PO to sign off: an agent must not approve in the PO's name.

### Changed
- Gates, approvals and staleness flags use the initiative's track.
- Approving or reopening a file in `handoff/`, `adhoc/` or `reviews/` now logs to the initiative's approvals log, not a stray log in the subfolder.
- An approved artefact whose upstream isn't approved now shows `upstream '<stage>' is <STATUS>`. Before, it always said "reopened", which was misleading after a track change.
- Ledger output is forced to UTF-8. On Windows, piped output used to crash on characters like ✔.
- The PRD rubric checks for stable IDs with BDD acceptance.

## [1.1.0] - 2026-11-21

Quick wins from the template review: tighter enforcement, code-based traceability, easier onboarding.

### Added
- `pdlc.py trace <slug>`: a code-based traceability check that reports requirement → story → test coverage, gaps, orphaned IDs, untested PRD scenarios and area-code clashes across initiatives. `--strict` exits non-zero, for CI.
- **Release gate enforces traceability**: `pdlc.py check <slug> release` blocks while any Must requirement has no story or no test scenario. `/override` still works, with a logged reason.
- `pdlc.py context-check`: lists context files that still have template placeholders. Every stage gate for real work (under `work/`) now warns until the required context is filled in.
- `/onboard`: an interview that fills in the product and team context files. You can paste existing material instead.
- `scripts/test_guard.py`: 18 simulated tool calls that prove the sign-off guard's rules, run by `/setup-check`.
- `docs/cheatsheet.md`: a one-page command guide organised by "I want to…".

### Changed
- **The sign-off guard now covers PowerShell.** Before, the hook only checked Bash, so on Windows an agent could modify an approved artefact through the PowerShell tool. The permission rules now also prompt for `pdlc.py approve|reopen|override` run from PowerShell.
- **Shell writes to approved files are now blocked** (Bash and PowerShell): redirects, in-place edits, moves, deletes, copies over the file, and script one-liners. Before, a shell command was only blocked if it mentioned sign-off fields. Reading or copying *from* an approved file is still allowed.
- `/trace` runs the code-based check first; `--deep` adds the `traceability-report` agent's judgement.
- `/setup-check` adds checks for guard logic, a live shell block, traceability and context.
- README links to the cheatsheet and agents overview, and the quick start uses `/onboard`.
- `.gitignore` explains how to version-control `work/` in a project copy.

## [1.0.0] - 2026-11-21

First version of the template, built from the PO Agent Kit.

### Added
- Stable requirement IDs (`<AREA>.<GROUP>.<ITEM>`) and BDD acceptance in the PRD, backlog and test-scenario templates, with BDD writing rules.
- Agents ported from CompanyName_placeholder's PDLC: `acceptance-coverage-check`, `traceability-report`, `three-amigos-facilitator`, `glossary-sync`. Commands: `/coverage`, `/trace`, `/three-amigos`.
- `context/status-legend.md`, `context/policies/`, and `.claude/agents/AGENTS-OVERVIEW.md`.
- The worked example migrated to stable IDs (area code `SET`).

### Changed
- Context files reset to placeholders. The worked example's filled-in context moved to `examples/flexpay-early-upgrade/context-snapshot/`.
