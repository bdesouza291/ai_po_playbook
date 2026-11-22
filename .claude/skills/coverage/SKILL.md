---
name: coverage
description: "Check a PRD's functional requirements for acceptance-scenario gaps, ambiguous language, malformed BDD and missing edge cases, before sign-off."
argument-hint: <slug or path to PRD>
---

Delegate to the `acceptance-coverage-check` subagent.

Resolve the PRD path from `$ARGUMENTS` (a slug means `work/<slug>/04-prd.md`; a path is used directly). Pass the PRD path and the initiative's `context/` files.

Show the PO the coverage percentage, the gaps (requirements with no acceptance), the top ambiguity and format issues, and the ordered recommendations. The subagent proposes only; if the PO wants changes, re-run `/prd <slug>` with the points as feedback so the `prd-writer` makes them.
