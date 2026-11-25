# Agents overview

A reference for every subagent defined in this repo: what it is for, when to trigger it in the PDLC and what it expects as input, and what it produces and where that output is used next.

> This file is documentation only — it has no agent front matter, so Claude Code does not load it as an agent. The real agent definitions are the other `*.md` files in this folder.
>
> Golden rule throughout: **agents draft, the PO approves.** No agent changes sign-off status; only `/approve`, `/reopen`, `/override` (via `scripts/pdlc.py`) do, and a stage can only start when its upstream artefacts are APPROVED.

## Core stage agents (the 13-stage flow)

These run one per PDLC stage, each invoked by its slash command, each producing one numbered artefact in `work/<slug>/`.

| Agent | Designed for | When to trigger — PDLC step & expected input | Output & where it is used next |
|---|---|---|---|
| `discovery-researcher` | Turning raw evidence into graded findings, jobs-to-be-done and pain points, honest about gaps | **Stage: discovery** (`/discover`), after the **brief** is APPROVED. Expects: `00-brief.md` and raw evidence in `work/<slug>/inputs/` (interviews, tickets, survey exports, analytics CSVs, app reviews, competitor notes) | `01-discovery.md` — findings graded Strong/Moderate/Weak. Feeds the **opportunity** stage |
| `opportunity-framer` | Framing the problem, target outcomes, sizing (low/likely/high) and the riskiest assumptions to test | **Stage: opportunity** (`/frame`), after **discovery** is APPROVED. Expects: `01-discovery.md`, the brief, and inputs for sizing data | `02-opportunity.md` — problem statement, outcomes, sized value, hypotheses. Feeds **prioritisation** and sets the goals the PRD copies |
| `prioritisation-analyst` | Comparing options transparently (RICE/WSJF), recommending one and slicing an MVP | **Stage: prioritisation** (`/prioritise`), after **opportunity** is APPROVED. Expects: `02-opportunity.md` (and discovery for context) | `03-prioritisation.md` — scored options, recommendation, MVP slice. Defines the scope the PRD is written against |
| `prd-writer` | Writing the PRD: stable-ID requirements with BDD acceptance, NFRs, risks, compliance questions | **Stage: prd** (`/prd`), after **prioritisation** is APPROVED. Expects: `02-opportunity.md`, `03-prioritisation.md`, discovery; `context/*` files | `04-prd.md` — requirements `SET.<group>.<item>` + scenarios. The spine of the whole chain: feeds metrics, backlog, test; its IDs flow downstream |
| `metrics-analyst` | Building the metric tree, tracking plan and A/B design (plan mode); later reading results (review mode) | **Stage: metrics** (`/metrics`) after **prd** APPROVED, and again at **post-launch** (`/post-launch`) after release. Expects: `04-prd.md` for the goals; for post-launch, `05-metrics-plan.md` + `09-release-plan.md` + results in `inputs/` | `05-metrics-plan.md` (events, sample size, guardrails) → feeds backlog instrumentation, release and post-launch. Later `11-post-launch-review.md` (the verdict) |
| `story-writer` | Breaking the PRD into epics and INVEST stories with tagged Gherkin and full traceability | **Stage: backlog** (`/stories`), after **prd** and **metrics** are APPROVED. Expects: `04-prd.md` (requirement IDs), `05-metrics-plan.md` (analytics events); DoR in the team context | `06-backlog.md` — stories that *Deliver* requirement IDs and tag scenarios `SET.…`. Feeds test, refinement and release |
| `qa-scenario-designer` | Designing test scenarios (happy/negative/edge/a11y/analytics/audit) and finding AC gaps | **Stage: test** (`/test-scenarios`), after **backlog** is APPROVED. Expects: `06-backlog.md` (and the PRD for rules/NFRs) | `07-test-scenarios.md` — scenarios keyed to requirement IDs + coverage table. Gaps feed back to the backlog; feeds refinement and release |
| `refinement-facilitator` | Preparing a refinement session (agenda, pointed questions, split options) and capturing outcomes | **Stage: refinement** (`/refine`), after **backlog** and **test** are APPROVED. Expects: `06-backlog.md`, `07-test-scenarios.md` | `08-refinement-pack.md` — questions and proposed story changes. Drives updates back into the backlog before Execute |
| `release-planner` | Planning a phased rollout with go/no-go, monitoring and rollback triggers | **Stage: release** (`/release`), after **backlog**, **test** and **metrics** are APPROVED. Expects: those three artefacts | `09-release-plan.md` — rollout phases, checklist, stop rules. Feeds comms and post-launch |
| `stakeholder-comms` | Writing audience-specific updates: exec, internal, customer copy, support brief | **Stage: comms** (`/comms`), after **release** is APPROVED. Expects: `09-release-plan.md` (and PRD/metrics for substance) | `10-comms.md` — ready-to-adapt messages. Used to announce and support the release |
| `metrics-analyst` *(review mode)* | Reading the launch results against the plan and giving an honest verdict | **Stage: post-launch** (`/post-launch`), after **metrics** and **release** are APPROVED and results exist. Expects: `05-metrics-plan.md`, `09-release-plan.md`, results in `inputs/` | `11-post-launch-review.md` — did it work, what moved, what next. Closes the loop; informs the next opportunity |
| `build-spec-writer` | Writing a **self-contained build spec for one story**, so a developer or an AI coding agent can build it without other documents: verbatim requirements and tagged acceptance criteria, out of scope, test intent, builder context, rules for AI agents | **Handoff** (`/handoff <slug> <story-id>`), per story, after **backlog**, **test** and (full track) **refinement** are APPROVED. Expects: the verbatim extract from `pdlc.py story`, the PRD, sibling stories, the test plan, team DoD | `handoff/<story-id>.md` — handed to the dev team or an AI coding agent once approved and the tech lead has filled the `[[TECH LEAD]]` gaps. Its scenario IDs come back on the tests, feeding **close** |
| `close-analyst` | Reconciling what shipped against the PRD's requirement and scenario IDs, finding drift, and turning every gap into a follow-up or a decision | **Stage: close** (`/close <slug> <evidence>`), once delivery evidence exists (CI JUnit XML, manual test logs, test folders), after **backlog** and **test** are APPROVED. Expects: `pdlc.py trace --evidence` output (source of truth), PRD, backlog, test plan, build specs, PR build logs in `inputs/` | `12-close-report.md` — Close / Close with follow-ups / Not ready. Follow-up stories go to the backlog via `/reopen` + `/stories`; drift items become PRD reopens |

## Cross-cutting agents (used across stages, not tied to one gate)

These are quality, traceability and support agents. They **read and report** (or write ad-hoc notes); they never advance the flow.

| Agent | Designed for | When to trigger — PDLC step & expected input | Output & where it is used next |
|---|---|---|---|
| `artefact-critic` | An independent rubric review of any draft, spot-checking numbers and claims | After any draft, **always run automatically after prd, backlog and release**; offered elsewhere (`/critique <path>`). Expects: the artefact path + its upstream artefacts + `context/quality-rubrics.md` | A review file in `work/<slug>/reviews/` — verdict and top issues. The PO uses it to decide approve vs revise |
| `acceptance-coverage-check` | Checking a PRD's requirements for acceptance gaps, ambiguity and malformed BDD | Right **after a PRD draft, before sign-off** (`/coverage <slug>`). Expects: `04-prd.md` + `context/*` | Coverage report (gaps, ambiguity, format issues, recommendations). Points the `prd-writer` to fixes before `/approve` |
| `traceability-report` | Judging whether the requirement → story → test chain is *genuinely* sound: does a story really deliver what it claims? The counting (gaps, orphans, coverage) is done by `pdlc.py trace`, which runs first | **Before refinement or release** (`/trace <slug> --deep`), once backlog and/or test exist. Expects: `04-prd.md`, `06-backlog.md`, `07-test-scenarios.md` + the `pdlc.py trace` output | Coverage report + verdict (ready / not ready). Gaps route to `/stories` or `/test-scenarios`; gives confidence to proceed to release |
| `three-amigos-facilitator` | A structured PO/Dev/QA deep-dive on one tricky story or requirement | **Around the refinement step** (`/three-amigos <slug> <id>`), or any time a story needs sharpening. Expects: a story/requirement ID + `06-backlog.md`/`04-prd.md` + `context/*` | `work/<slug>/adhoc/three-amigos-<id>.md` — sharpened AC, prioritised risks, open questions. Feeds the refinement pack / backlog |
| `glossary-sync` | Keeping domain language consistent; proposing glossary additions | **After a PRD or backlog draft**, or when terms drift. Invoke via `/ask-agent`. Expects: the artefact + `context/glossary.md` | A proposals list (new terms, inconsistencies). The PO applies accepted terms to `context/glossary.md` |
| `meeting-scribe` | Turning meeting notes into decisions, actions and proposed artefact changes | **Any time** a relevant meeting happens (`/meeting`). Expects: raw meeting notes | Meeting notes written to `work/<slug>/inputs/` plus decisions/actions. Proposed changes feed the relevant stage artefact |

## How the chain fits together

```
FULL TRACK
brief ▶ discovery ▶ opportunity ▶ prioritisation ▶ PRD ▶ metrics ▶ backlog ▶ test ▶ refinement ▶ handoff (per story) ▶ build ▶ close
                                                                              │
                                                                              └▶ release (also needs metrics) ▶ comms
                                                                                    └▶ post-launch (also needs metrics)

LITE TRACK
brief ▶ PRD ▶ backlog ▶ test ▶ handoff (per story) ▶ build ▶ close

"build" is the dev team or an AI coding agent working from approved build specs. It sits outside the kit.
Exact gates for either track: scripts/pdlc stages --track <full|lite>
```

- **Tracks:** each initiative runs on `full` or `lite`, chosen at `/new-initiative` and changed with `/track`. On lite, skipped stages pass their gate through: the PRD gates on the brief, the backlog on the PRD. Agents are told which stages were skipped and mark missing inputs `[[OPEN]]`.

- **Stable IDs** allocated in the PRD (`SET.<group>.<item>`) are carried by `story-writer` into the backlog, by `qa-scenario-designer` into test scenarios, by `build-spec-writer` into each build spec, and back by the builders onto every test. `close-analyst` reads them off the delivery evidence. `pdlc.py trace` checks the chain at every step; `acceptance-coverage-check` checks each requirement is acceptance-complete.
- Every stage artefact stops at a **PO sign-off gate**. The cross-cutting agents inform those decisions but never make them.
- The **release gate** is also code-enforced: it stays blocked while any Must requirement has no story or test scenario.
- See `CLAUDE.md` for the stage run protocol and the full stage/gate table, `context/status-legend.md` for how status words relate to the ledger gate, and `docs/cheatsheet.md` for a one-page command guide.
