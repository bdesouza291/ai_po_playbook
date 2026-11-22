---
initiative: flexpay-early-upgrade
stage: refinement
status: APPROVED
version: 1
produced_by: refinement-facilitator
upstream: 06-backlog.md, 07-test-scenarios.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-11-18 17:30
approved_hash: 9c03cb693ace9291
---
# Refinement pack: Self-serve settlement figure (session 1)

## Session goal
Get EU1-S1, EU1-S3, EU2-S2 and EU3-S1 ready for sprint 1 planning, and agree how to split EU2-S1.

## Proposed agenda (60 minutes)
| Time | Item |
|---|---|
| 0-5 | Context: why this, the A/B test, the spring deadline |
| 5-20 | EU1-S1 and the Agreement Service spike |
| 20-30 | EU1-S3 error and ineligible states |
| 30-40 | EU2-S1: split options |
| 40-50 | EU2-S2 and EU3-S1 (quick) |
| 50-60 | Estimate what's ready, agree actions |

## Stories to bring, in order
| Story | Why now | Readiness | Questions to resolve in the room |
|---|---|---|---|
| EU1-S1 | Everything depends on it | Designs pending | Real-time figure: what latency do we get today? |
| EU1-S3 | Same component, must ship together | Designs pending | Do arrears and dispute flags come back in the same call? |
| EU2-S1 | Biggest unknown | Looks large | Does the upgrade journey accept a figure passed in? |
| EU2-S2 | Must-have, small | Needs support URL | None if URL is confirmed |
| EU3-S1 | Needed before test starts | Ready | Which event library version? |

## Questions for engineering
1. Does the Agreement Service return a settlement figure in real time, or only via the CRM-triggered batch?
2. What's its 95th percentile response time today?
3. Are arrears, dispute and support flags on the same endpoint?
4. Does the Agreement Service already log every figure it generates (NFR-03)?
5. Can the upgrade journey take a settlement amount as input, or does it fetch its own?

## Questions for design
1. Where does the card sit on the hub on a 320px screen?
2. How do we show "valid until" so it's not missed?

## Questions for stakeholders (to resolve before the session)
- Compliance partner: draft card copy and validity period (PRD open question 1).
- Customer Ops lead: support page URL and phone line for EU2-S2.

## Dependency and risk map
| Dependency | Story | Owner | Risk if late |
|---|---|---|---|
| Agreement Service real-time | EU1-S1, S3 | Backend lead | Blocks everything |
| Compliance copy | EU1-S1, S5, EU2-S2 | Compliance partner | Blocks release, not build |
| Upgrade journey change | EU2-S1 | Upgrade journey team | Blocks handoff; test could run with hub link only |
| Data engineering | EU3-S2, S3 | Data lead | Blocks test start |

## Stories likely to be too big, with split options
**EU2-S1**
1. By path: (a) figure carried to summary, (b) refresh on expiry, (c) service-down at refresh.
2. By approach: (a) link into the journey and let it fetch its own figure (no change to the journey), (b) pass the figure in later.

## Definition of Ready gaps
- Designs for EU1-S1, S2, S3, S5 and EU2-S2.
- Support page URL for EU2-S2.
- Story for NFR-03 audit logging, pending engineering answer to question 4.

## After the session
### Proposed backlog changes (from session notes, 18 Nov)
| Story | Field | Old | New | Reason |
|---|---|---|---|---|
| EU2-S1 | Split | One story | EU2-S1a (link and journey fetches its own figure), EU2-S1b (refresh on expiry) | Team chose split option 2 |
| New | Story | - | EU1-S6: Log every generated figure for audit | Agreement Service doesn't log today |
| EU1-S3 | Notes | - | Flags are on the same endpoint | Engineering answer to Q3 |

Source: `inputs/meeting-2025-11-18-refinement.md`.
