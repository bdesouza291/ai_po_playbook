---
name: onboard
description: "Set the kit up for a new project or role: a short interview that fills in the product and team context files every agent reads."
argument-hint: "[product | team | regulatory | all]"
disable-model-invocation: true
---

Fill in the context files that every agent reads before drafting. Default scope is `all`; `$ARGUMENTS` can narrow it to `product`, `team` or `regulatory`.

1. Run `python3 scripts/pdlc.py context-check` (or `python ...` on Windows) and show the PO which files still have placeholders. Do the REQUIRED files first: `context/product-context.md`, then `context/team-and-ways-of-working.md`.
2. For each file, work through its headings in order. Ask **one question at a time**, using AskUserQuestion with sensible options where the answer is a choice (sprint length, estimation method, accessibility bar), free text otherwise. Offer to paste in existing material instead: a strategy deck, a team wiki page, a Definition of Done. If they paste, extract the answers from it and confirm them.
3. Write the answers into the file in the PO's own words, replacing each `<placeholder>`. Tidy the grammar only. Don't invent facts, numbers or system names. If the PO says "skip" or "don't know", leave `[[OPEN]]` in place of the placeholder.
4. Keep what the template says about stable IDs, the Definition of Ready and Done structure, and the guidance notes in `>` quotes, unless the PO asks to change them.
5. The **Product Owner name** in the team file matters: it is stamped as owner on every artefact. Confirm the spelling.
6. For `regulatory`, list the PO's sector obligations as **questions for Compliance**, never as statements of law. Point them at `context/policies/` for full policy documents.
7. Finish by re-running `context-check` and showing the result. Then suggest the next step: `/new-initiative <slug> "<idea>"`.

Filled-in examples of every file are in `examples/flexpay-early-upgrade/context-snapshot/` if the PO wants to see what good looks like.
