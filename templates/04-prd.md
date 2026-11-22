---
initiative: {{slug}}
stage: prd
status: DRAFT
version: 1
produced_by: prd-writer
upstream: 02-opportunity.md, 03-prioritisation.md
owner:
approved_by:
approved_at:
approved_hash:
---
# PRD: <title>

| | |
|---|---|
| PO | |
| Status | Draft |
| Stakeholders | |
| Target release | |
| **Area code** | `<AREA>` — short uppercase code for this capability, e.g. `UPG`. Used as the root of every stable requirement ID below. |

## 1. Problem and context
## 2. Goals and success measures
| Goal | Metric | Baseline | Target | By when |
|---|---|---|---|---|

## 3. Non-goals
## 4. Users and scenarios
## 5. Scope
### In scope (MVP)
### Out of scope
## 6. User journey
<!-- Step-by-step happy path, then key alternative paths. Mermaid flowchart welcome. -->

## 7. Functional requirements

> **Stable ID format** — carried through to stories, test scenarios, PRs and tests. Do not reuse or renumber an ID once it has been referenced anywhere downstream.
> - Requirement: `<AREA>.<GROUP>.<ITEM>` — e.g. `UPG.010.010`
> - Scenario: `<AREA>.<GROUP>.<ITEM>.<SCN>` — e.g. `UPG.010.010.010`
> - Increment by `010`; use `011`–`019` for later insertions between existing IDs.
> Every requirement must have at least one acceptance scenario.

### Requirements index
| ID | Requirement | Priority (MoSCoW) |
|---|---|---|

### Requirement detail

<!-- Repeat this block per requirement. Group by GROUP (010, 020, …) for distinct areas of behaviour. -->

**`<AREA>.010.010` — <short requirement name>** · Priority: Must / Should / Could / Won't
<requirement statement — what outcome is required, implementation-neutral>

- **Acceptance (BDD)**
  - **`<AREA>.010.010.010` — <scenario title>**
    - Given <context / precondition>
    - When <single action>
    - Then <single observable outcome>
  - **`<AREA>.010.010.020` — <negative or edge scenario title>**
    - Given <context>
    - When <action>
    - Then <outcome>

**Rules / notes:** <business rules, validation, data constraints for this requirement>

## 8. Business rules
## 9. Non-functional requirements
<!-- Performance, availability, accessibility (WCAG 2.2 AA), security, privacy (UK GDPR), audit, analytics. -->
## 10. Data and integrations
<!-- What data the product needs, from where. Name systems, not API designs - the team owns the design. -->
## 11. Regulatory and compliance considerations
<!-- Prompts to confirm with compliance. Not legal advice. -->
## 12. Content and comms needs
## 13. Dependencies
## 14. Risks and mitigations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|

## 15. Release approach
## 16. Open questions
| # | Question | Who can answer | Needed by |
|---|---|---|---|

## Assumptions the agent made

---

## Appendix: BDD acceptance writing rules
Apply these to every Given/When/Then scenario in this PRD and downstream.

**Style**
- Use explicit actor phrasing in every step: `Given the <actor> ...`, `When the <actor> ...`.
- One primary action per `When` step. One observable outcome per `Then`/`And`.
- Keep implementation detail out of step text — no API endpoints, CSS/HTML, framework names, or technical identifiers.
- Use en-GB spelling. Avoid contractions.

**Structure**
- One scenario tests one behaviour. Prefer several focused scenarios over one compound scenario.
- `Given` describes a state or precondition, not a sequence of actions.
- Use parameterised placeholders where values vary rather than hardcoding strings.

**So that automation maps cleanly**
- Write each step so it maps to one action (Given/When) or one check (Then) in downstream test automation.
- Use a consistent verb vocabulary across all scenarios.
