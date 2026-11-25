---
name: new-initiative
description: "Start a new initiative. Creates work/<slug>/, sets its track (lite by default, or full) and helps the PO write the brief through a short interview."
argument-hint: <slug> "<one-line title or idea>" [lite|full]
disable-model-invocation: true
---

Arguments: `$ARGUMENTS` (first word is the slug, the rest is the title or idea, optionally ending in `lite` or `full`).

1. **Choose the track** if it wasn't given. Use AskUserQuestion, with **lite first and marked as the default** (`scripts/pdlc init` also defaults to it):
   - **lite (default)** (brief > PRD > backlog > test > close): small, low-risk changes, internal tools, spikes.
   - **full** (all 13 stages): opt in when the work is customer-facing, regulated, measured with an experiment, or needs stakeholder comms.
   The PO can switch later with `/track`. If they are unsure, recommend lite, and full as soon as any of the full criteria apply.
2. Run `scripts/pdlc init <slug> --title "<title>" --track <track>`.
3. Interview the PO to fill `work/<slug>/00-brief.md`. Ask **one question at a time**, at most six, following the brief's headings. Use AskUserQuestion with sensible options where it helps, free text otherwise. If the PO says "skip", leave the section with `[[OPEN]]`. On the **lite** track the PRD is drafted straight from the brief, so press a little harder on "What good looks like" and "Out of scope".
4. Write their answers into the brief in their own words. Tidy grammar only; don't add claims they didn't make.
5. Tell the PO to drop evidence into `work/<slug>/inputs/`, and that the brief needs their `/approve` before the next stage can run: `/prd` on lite, `/discover` on full.
