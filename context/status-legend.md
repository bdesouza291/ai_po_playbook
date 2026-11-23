# Status legend

Two things track status in this kit, and they are deliberately separate:

1. **The sign-off ledger** (`scripts/pdlc.py`) is the source of truth for the gate. It only knows two states that matter for gating: **DRAFT** and **APPROVED** (plus the derived `CHANGED SINCE APPROVAL` and `STALE` flags). Nothing moves downstream until the upstream artefact is APPROVED in the ledger.

2. **The `Status` line a human reads** inside each artefact can be more expressive, to show where a draft is socially. The richer vocabulary below is adapted from established PDLC practice. Use it in the body/header of an artefact for communication; it never changes the gate — only `/approve` does that.

> Rule of thumb: the ledger says *can the next stage start?*; the status word says *how settled is this draft?*

## Shared draft-stage vocabulary (any artefact)

| Status word | Meaning | Ledger state |
|---|---|---|
| Draft | Being authored; not circulated | DRAFT |
| In Review | Shared with named reviewers for structured feedback | DRAFT |
| In Socialisation | Shared with a wider group for awareness and input | DRAFT |
| In Refinement | Active changes in response to feedback; not yet stable | DRAFT |
| Gate Decision Pending | Complete; awaiting the PO's go/no-go | DRAFT |
| Approved | Gate passed; downstream work can begin | APPROVED |
| Parked / Deferred | Revisit later; holding conditions recorded | DRAFT |
| Superseded | A newer version has replaced this one | (reopened → new version) |

## Artefact-specific notes

- **00 Brief / 02 Opportunity:** a brief can also end **Rejected** (opportunity not pursued; archive it).
- **04 PRD / 06 Backlog:** once requirements carry stable IDs and stories reference them, prefer `In Refinement` over silent edits — reopening (`/reopen`) is how an APPROVED PRD legitimately changes, which bumps the version and marks downstream artefacts `STALE`.
- **06 Backlog stories** may additionally carry a delivery state the team owns outside this kit: *Ready for Development → In Development → In QA → Done*. Those live in your tracker (Jira/ADO), not in the ledger.
- **09 Release:** use `Gate Decision Pending` while the go/no-go checklist is open.
- **Build specs (`handoff/<story-id>.md`)** are signed off one by one, like any artefact. Approve one only after the tech lead has filled its `[[TECH LEAD]]` gaps.
- **Delivery status per requirement** comes from `pdlc.py trace <slug> --evidence <paths>`, not from anyone's judgement:
  - *Implemented (full)*: every scenario of the requirement has a passing test.
  - *Implemented (partial)*: some pass.
  - *Tests found, no passing result*: tests mention the ID but there's no result file.
  - *No evidence*: nothing at all.

  The close report (`12-close-report.md`) records these.

## Tracks

| Track | Stages | Shown in `/status` as |
|---|---|---|
| full | all 13 stages | every stage listed |
| lite | brief, PRD, backlog, test, close (+ build specs) | the others show `SKIPPED (lite)` |

A track change is a PO decision, made with `/track` and logged in the approvals log.

## The ledger's derived flags (shown by `/status`)

| Flag | What it means | What to do |
|---|---|---|
| `CHANGED SINCE APPROVAL` | The file was edited after it was approved (content hash no longer matches) | Re-approve, or reopen to version it properly |
| `STALE` | An upstream artefact was reopened and re-approved after this one was approved | Revisit this artefact against the new upstream |
| `GATE BLOCKED` | Upstream isn't APPROVED yet | `/approve` the upstream, or `/override` with a reason |
