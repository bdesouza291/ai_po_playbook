# AI PO playbook: using agents across the whole role

The kit covers the build flow from brief to post-launch. A PO's week is wider than that. This is the full map: where agents help, which part of the kit does it (or what to build next), and what stays with you.

The rule of thumb throughout: **agents do the first 80% of the writing, the searching and the arithmetic. You do the judgement, the relationships and the decisions.**

---

## 1. Discovery and customer understanding
| Use | How | In the kit? |
|---|---|---|
| Synthesise interviews, tickets, reviews and survey verbatims into graded findings | `discovery-researcher` | `/discover` |
| Write an interview guide or survey from your open questions | `/ask-agent discovery-researcher` | Ad hoc |
| Turn a CRM or contact-reason export into a ranked pain list | Agent + Python for counts | `/discover` |
| Monthly "voice of customer" digest from new reviews and complaints | Scheduled run of the researcher on a refreshed `inputs/` folder | Build next |
| Desk research on competitor journeys | Researcher with web access, labelled as desk research | `/discover` |

**Keep for yourself:** talking to customers. Agents can prepare you and summarise afterwards; they can't replace sitting with someone who's frustrated.

## 2. Strategy, sizing and prioritisation
| Use | How | In the kit? |
|---|---|---|
| Problem framing, opportunity trees, hypotheses | `opportunity-framer` | `/frame` |
| Business case sizing with ranges and labelled assumptions | `opportunity-framer` | `/frame` |
| Option generation and RICE / WSJF scoring with inputs shown | `prioritisation-analyst` | `/prioritise` |
| Quarterly roadmap draft from approved opportunities | New `roadmap-planner` agent reading all initiatives' approved opportunity docs | Build next |
| "Pre-mortem" on a plan: how could this fail? | `/ask-agent artefact-critic` with a pre-mortem prompt | Ad hoc |

**Keep for yourself:** the call on what matters most, and the conversation with whoever disagrees.

## 3. Requirements and backlog
| Use | How | In the kit? |
|---|---|---|
| PRD / spec from approved scope | `prd-writer` | `/prd` |
| Epics and stories with Gherkin AC, DoR checks, traceability | `story-writer` | `/stories` |
| Split a story that's too big | `/ask-agent story-writer` | Ad hoc |
| Backlog hygiene: duplicates, stale items, stories missing AC | New `backlog-auditor` agent run against a Jira export | Build next |
| Data mapping and migration requirements (field by field) | `/ask-agent prd-writer` with source and target schemas in `inputs/` | Ad hoc |
| Non-functional and accessibility requirements checklist | Built into PRD template and rubric | `/prd` |

**Keep for yourself:** saying no, and choosing what *not* to build.

## 4. Delivery and ceremonies
| Use | How | In the kit? |
|---|---|---|
| Refinement prep: questions, risks, split options | `refinement-facilitator` | `/refine` |
| Turn refinement or planning notes into proposed story changes | `meeting-scribe` | `/meeting` |
| Sprint goal options from the top of the backlog | `/ask-agent refinement-facilitator` | Ad hoc |
| Sprint review talking points: learning, not just output | `stakeholder-comms` | `/comms` |
| Test scenarios and AC gap-finding before build | `qa-scenario-designer` | `/test-scenarios` |
| Release plan, go / no-go, rollback triggers | `release-planner` | `/release` |

**Keep for yourself:** being present in the room, accepting stories, and unblocking people.

## 5. Stakeholder management and communication
| Use | How | In the kit? |
|---|---|---|
| Exec updates, release notes, support briefings | `stakeholder-comms` | `/comms` |
| Prep for a hard conversation: their likely objections and your answers | `/ask-agent stakeholder-comms` | Ad hoc |
| Saying no well: a reply that explains the trade-off | `/ask-agent stakeholder-comms` | Ad hoc |
| Weekly status from approved artefacts and `/status` | New `/weekly-update` command | Build next |
| Decision log kept up to date from meetings | `meeting-scribe` proposes rows for `decisions.md` | `/meeting` |

**Keep for yourself:** trust. Send messages yourself, in your voice. Use drafts as a starting point.

## 6. Data, metrics and experiments
| Use | How | In the kit? |
|---|---|---|
| Metric trees, definitions, tracking plans | `metrics-analyst` (plan mode) | `/metrics` |
| Sample size and test duration, with the arithmetic shown | `metrics-analyst` runs Python | `/metrics` |
| Read-out of an A/B test with confidence intervals | `metrics-analyst` (review mode) | `/post-launch` |
| Ad-hoc analysis of a CSV export ("which segment drops most?") | `/ask-agent metrics-analyst` | Ad hoc |
| Funnel or KPI dashboard mock-up for the team | Ask Claude for a chart or dashboard page | Ad hoc |

**Keep for yourself:** deciding what "good" means before the data comes in.

## 7. Risk, compliance and quality
| Use | How | In the kit? |
|---|---|---|
| Regulatory questions to raise with Compliance for a change | Every agent uses `context/regulatory-notes.md` | Built in |
| Customer-harm review of an option (Consumer Duty lens) | `prioritisation-analyst` flags harm; `/ask-agent artefact-critic` for a deeper look | Built in |
| Independent review of any draft | `artefact-critic` | `/critique` |
| Audit trail of who approved what | `approvals-log.md` and fingerprints | Built in |

**Keep for yourself:** the compliance conversation itself. Agents ask good questions; Compliance answers them.

## 8. Your own effectiveness
| Use | How |
|---|---|
| Onboarding to a new domain: glossary, regulation primer, system map from documents | `/ask-agent discovery-researcher` on the onboarding pack; save results in `context/` |
| Meeting prep: one page on attendees' likely concerns and your asks | Ad hoc |
| Turning your rough thoughts into a clear brief | `/new-initiative` interview |
| Learning: quiz yourself on a new domain or framework | Ask Claude directly |

---

## A weekly rhythm that gets the time back

| When | What the agents do | What you do |
|---|---|---|
| Monday | `/status` across initiatives; draft the week's stakeholder update | Read, fix, send |
| Before refinement | `/refine` pack | Close DoR gaps, chase answers |
| After any meeting | `/meeting` with your notes | Accept or reject proposed changes |
| Mid-week | Draft the next stage for whichever initiative is waiting | Review, `/approve` or feedback |
| Friday | Digest of new evidence in `inputs/` | Decide what's worth acting on |

## How to tell if it's actually faster
"60% faster than peers" is a good ambition; measure it rather than assume it. For a month, note for each artefact:
- time to a first draft before (your estimate) and now,
- number of review rounds,
- issues found later that the review missed.

If review rounds or late issues go up, the agents are making you faster at producing work that isn't ready. Tighten the context files and rubrics before adding more agents.

## What to build next
1. **Jira / Confluence (or Azure DevOps) via MCP:** a `/publish` command that pushes approved stories and pages. Approval stays here.
2. **`backlog-auditor`:** reads a backlog export, finds duplicates, orphans, stories missing AC.
3. **`roadmap-planner`:** builds a now / next / later view from all approved opportunity docs.
4. **`/weekly-update`:** status digest from the approvals log and `/status`.
5. **Scheduled voice-of-customer digest:** runs the researcher weekly on new reviews and complaints.
