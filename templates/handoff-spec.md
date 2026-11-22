---
initiative: {{slug}}
stage: handoff
story: {{story-id}}
status: DRAFT
version: 1
produced_by: build-spec-writer
upstream: 06-backlog.md, 07-test-scenarios.md, 04-prd.md
owner:
approved_by:
approved_at:
approved_hash:
---
# Build spec: <story-id>: <story title>

> **For developers and AI coding agents.** This spec is self-contained: you should be able to build the story without opening any other document. Where something is ambiguous or missing, **stop and ask**; don't guess. Requirement and scenario IDs are permanent. Keep them exactly as written.

| | |
|---|---|
| Initiative | `<slug>` |
| Story | `<story-id>` |
| Delivers | `<AREA>.<GROUP>.<ITEM>`, … |
| Priority | Must / Should / Could |
| Depends on | `<other story IDs or external dependencies>` |
| Questions to | PO: `<name>` · Tech lead: `<name>` |

## 1. Goal
<The user story, verbatim, then two or three plain sentences on why it matters, taken from the PRD's problem and goals.>

## 2. Requirements delivered
<Each requirement block this story delivers, **verbatim** from `pdlc.py story`: ID, priority, statement, rules.>

## 3. Acceptance criteria
<Every scenario of the delivered requirements, **verbatim**, each tagged with its scenario ID. Include the story's own Gherkin, plus any PRD or QA scenarios for the same requirements that the story doesn't list. Mark those with `# from PRD` or `# from test plan`.>

```gherkin
@<AREA>.<GROUP>.<ITEM>.<SCN>
Scenario: <title>
  Given ...
  When ...
  Then ...
```

## 4. Business rules and constraints
| Ref | Rule or constraint | Applies how |
|---|---|---|
| BR-nn / NFR-nn | <verbatim from the PRD> | <what it means for this story> |

## 5. Out of scope
<What a reasonable builder might add but must not, including what sibling stories cover ("refresh on expiry is EU2-S1b") and the PRD's non-goals that touch this area.>

## 6. Test intent
Every automated test **must carry its scenario ID** (a Gherkin tag `@<ID>`, a test name starting `<ID> -`, or a trait or attribute), so delivery can be traced back. Test level is decided by what's being checked; ownership is decided by who's accountable.

| Scenario ID | What it proves | Level (unit / integration / e2e / manual) | Owner (Dev / QA) | Test data |
|---|---|---|---|---|

## 7. Context for the builder
| Area | Pointer |
|---|---|
| Systems involved | <named systems from the product context. Names only, no designs> |
| Existing behaviour to keep | <what must not change> |
| Designs | <link, or "no UI change", or `[[TECH LEAD]]`> |
| Code / modules | `[[TECH LEAD]]`: repo paths, services, feature flags |
| Data | <fields, sources, retention, sensitivity> |
| Analytics | <events from the tracking plan, with "no personal data" notes> |

## 8. Open questions
| # | Question | Owner | Blocks build? |
|---|---|---|---|

<Empty, or every row has an owner and the PO has accepted it for build.>

## 9. Definition of Done
- [ ] Every scenario in §3 has a test tagged with its scenario ID, and it passes.
- [ ] Nothing outside §2–§3 was built (§5 respected).
- [ ] <team DoD items from `context/team-and-ways-of-working.md`>
- [ ] Build log written (below) and linked from the PR.

---

## Rules for AI coding agents
1. Build only what §2 and §3 describe. Anything else is out of scope (§5), even if it looks helpful.
2. Tag every automated test with its scenario ID from §3. Don't invent new scenario IDs; if you think a scenario is missing, raise it as a question.
3. Don't change requirement wording, acceptance wording, IDs or business rules. If they're wrong or contradictory, stop and ask.
4. If a §7 pointer is `[[TECH LEAD]]` and you need it, or a §8 question blocks your work, stop and ask. Don't guess repo structure, APIs or data.
5. Keep a short **build log** in the PR description: decisions taken, assumptions, anything you couldn't do and why. It feeds the close-out.
6. Never mark the story done or approve your own work. A human reviews it.
