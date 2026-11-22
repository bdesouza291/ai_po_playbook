---
initiative: {{slug}}
stage: close
status: DRAFT
version: 1
produced_by: close-analyst
upstream: 06-backlog.md, 07-test-scenarios.md, 04-prd.md
owner:
approved_by:
approved_at:
approved_hash:
---
# Close report: <title>

| | |
|---|---|
| Evidence checked | <paths given to `pdlc.py trace --evidence`, and their date> |
| Delivery window | <first build to last merge> |
| Verdict | Close / Close with follow-ups / Not ready to close |

## 1. Summary
<Three to five lines: what was delivered, what wasn't, and the verdict. Plain words.>

## 2. Delivery against the PRD
<From `pdlc.py trace <slug> --evidence ...`. Copy the numbers; don't recount them.>

| Requirement | Priority | Passing | Implementation | Notes |
|---|---|---|---|---|

## 3. Scenarios without a passing test
| Scenario ID | Requirement | Evidence status | Why | Action |
|---|---|---|---|---|

## 4. Drift: what shipped differs from the spec
<Behaviour that was built differently from the PRD or build spec, found in the evidence, PR build logs or ops feedback. Each item becomes a proposed `/reopen` of the PRD, or a follow-up. Never a silent edit.>

| # | What the spec says | What shipped | Source | Proposed action |
|---|---|---|---|---|

## 5. Follow-up stories (drafts)
<One block per gap. New story IDs; reference the original requirement and scenario IDs, never reuse or renumber them. Draft only. They go into the backlog via `/reopen` and `/stories`.>

### <EPIC>-S<n>: <title>
**Delivers (PRD requirement IDs):** `<AREA>.<GROUP>.<ITEM>`
**Why:** <the gap from §2–§4>
```gherkin
@<AREA>.<GROUP>.<ITEM>.<SCN>
Scenario: ...
```

## 6. Descope decisions to record
| Requirement | Decision needed | Owner |
|---|---|---|

## 7. Evidence quality
<How trustworthy the evidence is: results files vs mentions only, tests without IDs, environments, dates.>

## Assumptions the agent made
## Open questions for the PO
