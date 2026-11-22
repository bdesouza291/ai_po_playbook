# PO Agent Kit: instructions for Claude

This project is a Product Owner's workbench. Specialist subagents in `.claude/agents/` draft artefacts across the product development lifecycle (PDLC). **The human Product Owner signs off every artefact.** Nothing is automated end to end.

## The golden rule
Agents draft. The PO approves. You never approve, reopen, override or change an initiative's track on the PO's behalf.
- Only `scripts/pdlc.py` changes sign-off status. Claude Code asks the PO before running `approve`, `reopen`, `override` or `track`.
- Only run those four sub-commands when the PO has invoked `/approve`, `/reopen`, `/override` or `/track` in the current turn.
- A hook (`.claude/hooks/guard.py`) blocks edits to APPROVED files and blocks writing `status: APPROVED`. Do not try to work around it. If it blocks you, tell the PO what you were trying to do.
- If the PO asks whether to tick "don't ask again" on an approval prompt, recommend against it.

## Python
Use `python3 scripts/pdlc.py ...`. If `python3` is not found (common on Windows), use `python scripts/pdlc.py ...` for the rest of the session.

## Stage map
Each initiative lives in `work/<slug>/`. A stage can start only when its upstream artefacts are APPROVED. The table shows the **full** track; `python3 scripts/pdlc.py stages --track <full|lite>` prints the effective gates for either.

| Stage | Command | Agent | Output | Needs approved |
|---|---|---|---|---|
| brief | `/new-initiative` | PO, helped by you | `00-brief.md` | - |
| discovery | `/discover` | discovery-researcher | `01-discovery.md` | brief |
| opportunity | `/frame` | opportunity-framer | `02-opportunity.md` | discovery |
| prioritisation | `/prioritise` | prioritisation-analyst | `03-prioritisation.md` | opportunity |
| prd | `/prd` | prd-writer | `04-prd.md` | prioritisation |
| metrics | `/metrics` | metrics-analyst (plan mode) | `05-metrics-plan.md` | prd |
| backlog | `/stories` | story-writer | `06-backlog.md` | prd, metrics |
| test | `/test-scenarios` | qa-scenario-designer | `07-test-scenarios.md` | backlog |
| refinement | `/refine` | refinement-facilitator | `08-refinement-pack.md` | backlog, test |
| release | `/release` | release-planner | `09-release-plan.md` | backlog, test, metrics |
| comms | `/comms` | stakeholder-comms | `10-comms.md` | release |
| postlaunch | `/post-launch` | metrics-analyst (review mode) | `11-post-launch-review.md` | metrics, release |
| close | `/close` | close-analyst | `12-close-report.md` | backlog, test (+ delivery evidence) |
| handoff (per story) | `/handoff <slug> <story>` | build-spec-writer | `handoff/<story-id>.md` | backlog, test, refinement |

Supporting commands: `/onboard`, `/track`, `/status`, `/next`, `/critique`, `/approve`, `/reopen`, `/override`, `/meeting`, `/ask-agent`, `/setup-check`. A one-page command guide for the PO is in `docs/cheatsheet.md`.

## Tracks
Each initiative runs on a track, chosen at `/new-initiative` and changed only by the PO with `/track`. It is recorded in the approvals log.
- **full**: all stages above.
- **lite**: brief > PRD > backlog > test > close (+ handoff). A skipped stage's upstream passes straight through: the PRD gates on the brief, the backlog on the PRD, and handoff on backlog and test.
- On lite, the agent for a stage may expect an upstream artefact that doesn't exist (for example, the `prd-writer` expects an opportunity and prioritisation). Tell it which stages were skipped. It works from the brief and `inputs/`, and marks missing goals, baselines, targets or scope decisions `[[OPEN]]` rather than inventing them.

## Build specs and close-out
- `/handoff` writes one **build spec per story** for developers or AI coding agents. Its story, requirement and acceptance sections come verbatim from `pdlc.py story <slug> <story-id>`. Never paraphrase them. `pdlc.py trace` warns when a spec's scenario tags drift from its story.
- `/close` reconciles delivery against the PRD. `pdlc.py trace <slug> --evidence <paths>` (JUnit XML results, test folders, feature files) is the source of truth for which scenarios pass. The close report drafts follow-up stories; they reach the backlog only via `/reopen` and `/stories`.

**First run on a new project:** if `pdlc.py check` prints a `WARNING` about context placeholders, tell the PO before drafting anything and offer `/onboard`. Agents drafting against blank context produce generic filler.

Quality and traceability helpers (read-only; they propose, the PO decides):
- `/coverage <slug>` → `acceptance-coverage-check`: gaps, ambiguity and BDD issues in the PRD, before sign-off.
- `/trace <slug>` → `python3 scripts/pdlc.py trace <slug>` (code-based coverage, gaps, orphans, area-code clashes); `--deep` adds the `traceability-report` agent's judgement on top. Trust the script's numbers; don't recount coverage by reading the files.
- `/three-amigos <slug> <id>` → `three-amigos-facilitator`: a structured deep-dive on one story or requirement.
- `glossary-sync` (via `/ask-agent`): proposes glossary additions from an artefact.

## Stable IDs and traceability
Requirements get a stable ID in the PRD and it is carried, unchanged, all the way down:

`PRD requirement (<AREA>.<GROUP>.<ITEM>)  →  story (delivers the ID, tags scenarios)  →  test scenario (<AREA>.<GROUP>.<ITEM>.<SCN>)`

- The PRD declares the `<AREA>` code once (header) and numbers requirements `010.010`, incrementing by `010`.
- IDs are **never reused or renumbered** once referenced downstream. Insert with `011`–`019`.
- Every requirement has at least one BDD acceptance scenario; the BDD writing rules are in the PRD template appendix and `context/writing-style.md`.
- `/trace` checks the chain holds; `/coverage` checks each requirement is acceptance-complete.
- **The release gate enforces traceability.** `pdlc.py check <slug> release` returns `GATE BLOCKED` while any Must requirement lacks a story or a test scenario. Point the PO to `/stories` or `/test-scenarios`, or `/override` with a reason.
- Area codes should be unique across initiatives. `pdlc.py trace` warns on a clash; pick a different code in the PRD before IDs are referenced downstream.
Status vocabulary (the social state of a draft vs. the ledger gate) is defined in `context/status-legend.md`.

## Stage run protocol (every stage command follows this)
1. **Find the initiative.** `work/<slug>/` (or `examples/<slug>/` for the worked example). If the slug is missing or unknown, run `pdlc.py status` and ask which one.
2. **Check the gate.** Run `python3 scripts/pdlc.py check <slug> <stage>` (for a build spec: `check <slug> handoff --story <story-id>`). When the gate opens, it also prints `TRACK:` and `UPSTREAM:` lines; use them in step 3.
   - `GATE BLOCKED`: stop. Tell the PO what is missing and which command fixes it (`/approve`, or `/override` with a reason if they really want to skip ahead).
   - `GATE OPEN (OVERRIDE ...)`: continue, and remind the PO the upstream isn't approved.
   - `GATE OPEN ... NEW DRAFT`: continue.
   - `GATE OPEN ... REVISION`: ask the PO for their feedback if they haven't given it, then continue.
3. **Brief the agent.** Delegate to the stage's subagent with: the slug, the output path, the template path, the version number (keep the current version for a revision), the upstream artefact paths, the inputs folder, the track, and any PO feedback word for word. For upstream, pass the files on the gate's `UPSTREAM:` line plus any other files the stage's skill lists **that exist**. On lite, also pass `00-brief.md` and name the skipped stages (see *Tracks*).
4. **Critique.** For `prd`, `backlog` and `release`, always run `artefact-critic` on the new draft. For other stages, including handoff and close, offer it. After a `prd` draft, also offer `/coverage`; after `backlog` or `test`, offer `/trace`.
5. **Hand back for sign-off.** Show the PO, briefly:
   - what was written and where
   - the agent's summary, assumptions and `[[OPEN]]` decisions
   - the critic's verdict and top issues, if run
   Then ask what they want to do: approve (`/approve <path>`), revise with feedback (re-run the stage command with feedback), or park it. Use AskUserQuestion if available.
6. **Do not start the next stage** in the same turn. The PO moves the work on.

## Revisions
When the PO gives feedback on a DRAFT, re-run the same subagent with the feedback. Don't hand-edit agent output yourself unless the PO asks for a small specific change.

## Ad-hoc work
The PO can ask any agent for one-off help outside the flow (for example a stakeholder email or quick story split) with `/ask-agent`. Write ad-hoc output to `work/<slug>/adhoc/` or `work/_adhoc/`, as DRAFT.

## Context files every agent reads
- `context/product-context.md`: product, customers, strategy, systems. The PO fills this in for each job (placeholder by default).
- `context/team-and-ways-of-working.md`: team, cadence, story conventions, DoR, DoD, PO name.
- `context/writing-style.md`: British English, plain, no AI-polish.
- `context/regulatory-notes.md`: prompts for Compliance, not legal advice. Points at `context/policies/` for the organisation's real policy documents.
- `context/quality-rubrics.md`: used by the critic.
- `context/glossary.md`: product and domain terms; `glossary-sync` proposes additions.
- `context/status-legend.md`: how the human-readable status words relate to the ledger gate.
- `context/policies/`: drop your organisation's policy documents here (README explains the shape). Empty by default.

## Things not to do
- Don't fabricate evidence, quotes or numbers. Label assumptions.
- Don't estimate story points for the team.
- Don't tell the PO something is compliant.
- Don't edit files in `inputs/` (raw evidence) except when the meeting-scribe writes meeting notes there.
