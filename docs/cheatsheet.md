# Cheatsheet

One page. Find what you want to do, run the command. `<slug>` is your initiative's folder name under `work/`.

## Getting started

| I want to… | Run |
|---|---|
| Check the kit works on this machine | `/setup-check` |
| Set the kit up for a new product or team | `/onboard` |
| See which context files still need filling in | `python scripts/pdlc.py context-check` |
| Start a new piece of work | `/new-initiative <slug> "One line about it"` (asks which track; **lite** is the default, choose **full** for customer-facing, regulated or experiment-driven work) |
| See which stages a track runs | `python scripts/pdlc.py stages --track lite` |
| See where everything is up to | `/status` (or `/status <slug>`) |
| Be told what to do next | `/next <slug>` |

## Moving work through the lifecycle

Each command drafts one artefact. You approve it before the next stage can start.

| I want to… | Run | Produces |
|---|---|---|
| Make sense of my evidence (interviews, tickets, data) | `/discover <slug>` | `01-discovery.md` |
| Frame the problem and size the opportunity | `/frame <slug>` | `02-opportunity.md` |
| Compare options and pick an MVP | `/prioritise <slug>` | `03-prioritisation.md` |
| Write the requirements (PRD) | `/prd <slug>` | `04-prd.md` |
| Plan how we'll measure it | `/metrics <slug>` | `05-metrics-plan.md` |
| Break it into user stories | `/stories <slug>` | `06-backlog.md` |
| Design the test scenarios | `/test-scenarios <slug>` | `07-test-scenarios.md` |
| Prepare a refinement session | `/refine <slug>` | `08-refinement-pack.md` |
| Plan the rollout | `/release <slug>` | `09-release-plan.md` |
| Write the stakeholder and customer comms | `/comms <slug>` | `10-comms.md` |
| Review results after launch | `/post-launch <slug>` | `11-post-launch-review.md` |
| Hand one story to developers or an AI coding agent | `/handoff <slug> <story-id>` | `handoff/<story-id>.md` |
| Check what was delivered against the PRD | `/close <slug> <test results or folder>` | `12-close-report.md` |

**On the lite track (the default)** you skip straight from the brief to `/prd`, and there's no discovery, opportunity, prioritisation, metrics, refinement, release, comms or post-launch stage. Opt in to **full** when the work is customer-facing, regulated or experiment-driven.

**To revise a draft:** run the same command again with your feedback after the slug, e.g. `/prd <slug> make the error states clearer`.

**Before an AI agent builds from a spec:** get the tech lead to fill every `[[TECH LEAD]]` gap and clear the blocking open questions. Then approve it.

## Signing off

| I want to… | Run |
|---|---|
| Approve a draft | `/approve <path>` |
| Change something I already approved | `/reopen <path>` (asks for a reason; bumps the version) |
| Skip a gate on purpose | `/override <slug> <stage>` (asks for a reason; logged) |
| Move an initiative between lite and full | `/track <slug> <full\|lite> "<reason>"` (logged) |

You'll get a permission prompt each time. That prompt **is** the sign-off. Don't tick "don't ask again".

## Checking quality

| I want to… | Run |
|---|---|
| Get an independent review of a draft | `/critique <path>` |
| Check every PRD requirement has proper acceptance criteria | `/coverage <slug>` |
| Check every requirement has a story and a test | `/trace <slug>` (add `--deep` for an agent's judgement too) |
| Deep-dive one tricky story with PO/Dev/QA lenses | `/three-amigos <slug> <story-id>` |
| Tidy up terminology | `/ask-agent glossary-sync <slug> check the PRD's terms` |

## Everything else

| I want to… | Run |
|---|---|
| Turn meeting notes into decisions and actions | `/meeting <slug>`, then paste the notes |
| One-off help from any agent (an email, a quick split) | `/ask-agent <agent> <slug or _adhoc> <what you need>` |
| Understand what each agent does | read `.claude/agents/AGENTS-OVERVIEW.md` |

## Rules of thumb

- **Evidence goes in `work/<slug>/inputs/`.** Agents read it; they never edit it.
- **Requirement IDs are forever.** `SET.010.010` never gets reused or renumbered. Insert new ones with `011`–`019`.
- **`[[OPEN]]`** marks a decision only you can make. Search for it before approving.
- **`STALE`** in `/status` means something upstream changed after you approved this. Revisit it.
- **Run a stage or two per session.** A whole run in one go will hit usage limits.
- **The release gate checks traceability.** It stays shut while any Must requirement lacks a story or a test scenario.
- **Tests must carry their scenario ID** (`@SET.010.010.010`, or the ID at the start of the test name). That's the only way `/close` can tell what was delivered.
