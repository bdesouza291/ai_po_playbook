# Team and ways of working

> Fill this in for your team. The PO named here is stamped as the owner on every artefact and is the only person the kit treats as able to sign off.
> A filled-in example lives in `examples/flexpay-early-upgrade/context-snapshot/team-and-ways-of-working.md`.

## People
- **Product Owner (signs off artefacts):** <your name>
- Team: <make-up, e.g. 3 backend, 2 frontend, 2 QA, 1 BA, 1 Scrum Master>
- Key stakeholders: <roles who review or decide — e.g. Head of X, Compliance partner, UX lead>

## Cadence
- <sprint length, when refinement and review happen>
- Estimation: <method, e.g. story points, Fibonacci>. Agents never estimate on the team's behalf; they may flag "looks large".

## Story conventions
- Format: As a / I want / so that. Acceptance criteria in Gherkin (Given / When / Then).
- Stories tie back to PRD requirements by **stable ID** (`<AREA>.<GROUP>.<ITEM>`); scenarios carry the scenario ID (`<AREA>.<GROUP>.<ITEM>.<SCN>`). See `context/status-legend.md`.
- Story IDs: `<EPIC>-S<n>`, e.g. `EU1-S3`. Epics: `<initiative code><n>`.
- Stories should be vertical slices a team can finish within a sprint.

## Definition of Ready
1. Story follows INVEST.
2. Acceptance criteria are testable and include at least one negative path.
3. Designs linked, or "no UI change" stated.
4. Dependencies named, with an owner.
5. Analytics events named, if the story touches a tracked journey.
6. Compliance need flagged (yes / no).
7. Delivers at least one PRD requirement ID, and that ID exists in the approved PRD.

## Definition of Done
1. AC met and demoed to the PO.
2. Automated tests added, tagged with the scenario ID; no open P1/P2 defects.
3. Accessibility checked to <your bar, e.g. WCAG 2.2 AA>.
4. Analytics events verified.
5. Release notes line written.
6. Feature behind a flag if customer-facing.

## Prioritisation defaults
- Default method: <e.g. value vs effort with a confidence factor (RICE-style); WSJF across teams>.
- <What always jumps the queue — e.g. regulatory deadlines, customer-harm fixes.>
