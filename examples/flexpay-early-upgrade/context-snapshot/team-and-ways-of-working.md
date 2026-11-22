# Team and ways of working

## People
- **Product Owner (signs off artefacts):** Breitner de Souza Eremita
- Team: 3 backend, 2 frontend, 2 QA, 1 BA, 1 Scrum Master, 1 Delivery Manager
- Key stakeholders (fictional roles for the example): Head of Digital Sales, Customer Operations lead, Credit Risk manager, Compliance partner, Finance business partner, UX lead

## Cadence
- Two-week sprints. Refinement mid-sprint, 60 minutes. Sprint review fortnightly with stakeholders.
- Estimation in story points (Fibonacci). Agents never estimate on the team's behalf; they may flag "looks large".

## Story conventions
- Format: As a / I want / so that. Acceptance criteria in Gherkin (Given / When / Then).
- IDs: `<EPIC>-S<n>`, e.g. `EU1-S3`. Epics `<initiative code><n>`.
- Stories should be vertical slices that a team can finish within a sprint.

## Definition of Ready
1. Story follows INVEST.
2. Acceptance criteria are testable, include at least one negative path.
3. Designs linked, or "no UI change" stated.
4. Dependencies named, with owner.
5. Analytics events named, if the story touches a tracked journey.
6. Compliance need flagged (yes / no).

## Definition of Done
1. AC met and demoed to the PO.
2. Automated tests added; no open P1/P2 defects.
3. Accessibility checked to WCAG 2.2 AA.
4. Analytics events verified in the debugger.
5. Release notes line written.
6. Feature behind a flag if customer-facing.

## Prioritisation defaults
- Default method: value vs effort with a confidence factor (RICE-style). WSJF when comparing across teams.
- Regulatory deadlines and customer-harm fixes override scoring.
