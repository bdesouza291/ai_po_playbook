---
initiative: flexpay-early-upgrade
stage: release
status: APPROVED
version: 1
produced_by: release-planner
upstream: 06-backlog.md, 07-test-scenarios.md, 05-metrics-plan.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2026-02-02 16:00
approved_hash: 4bfa585202764b19
---
# Release plan: Self-serve settlement figure

## What's going out
EU1-S1 to S5, EU2-S1a, EU2-S2, EU3-S1 to S3, and EU1-S6 (audit logging) behind flag `settlement_selfserve`. EU2-S3 (CRM record) and EU2-S1b (refresh on expiry) follow in the next sprint; until then the journey fetches its own figure, so there's no expiry gap.

## Rollout strategy
| Phase | Audience / % | Entry criteria | Exit criteria | Date |
|---|---|---|---|---|
| 0. Staff | Northwind staff on FlexPlan (about 400) | All P1 test scenarios passed; Compliance copy signed off | 5 working days, card error rate under 2%, no wrong figures reported | 16-20 Feb 2026 |
| 1. A/B | 50% of mid-contract customers | Phase 0 exit; dashboard live; support briefed | 4 weeks enrolment, at least 3,780 customers per arm | 26 Feb - 26 Mar 2026 |
| 2. Read-out | No change to split | 30-day conversion window closed | Decision per metrics plan | 27 Apr 2026 |
| 3. Full | 100% if decision is ship | Read-out approved by PO | - | From 4 May 2026 |

## Feature flags and kill switch
- `settlement_selfserve`: on/off and percentage by customer ID.
- Kill switch: turning the flag off returns all customers to today's "call us" message within 5 minutes. Owner: on-call engineer, PO informed.

## Go / no-go checklist
| Area | Check | Owner | Status |
|---|---|---|---|
| Product | AC met, PO accepted all stories in scope | PO | |
| Quality | TS-01 to TS-32 passed, no open P1/P2 | QA lead | |
| Data | Events verified; assignment export and weekly porting feed running | Data lead | |
| Ops | Support briefing done; contact reason "Viewed figure online" added | Customer Ops lead | |
| Compliance | Card, statement and help route copy signed off | Compliance partner | |
| Comms | Internal note and support FAQ approved | PO | |

## Monitoring in the first 72 hours
- Card error rate and reasons, hourly.
- Figure reconciliation: daily sample of 50 figures shown online checked against the Agreement Service log.
- Settlement calls from treatment customers, daily.
- Complaints coded "settlement", daily.

## Rollback plan and triggers
Turn the flag off if any of these happen:
- Any confirmed case of a wrong figure shown.
- Card error rate above 5% for 30 minutes.
- Port-out in treatment more than 3pp above control after 2,000 viewers per arm (metrics plan stop rule).

## Support readiness
- Briefing for contact-centre team leaders a week before Phase 1.
- FAQ: what the figure includes, how long it's valid, why some customers can't see it, how to pay.
- Customers in difficulty: existing financial support team and process, no change. Help route volume watched weekly.

## Known issues at launch
- Agents can't see a figure viewed online until EU2-S3 ships. Customers may quote a figure the agent can't see; agents generate a new one as today.

## Assumptions the agent made
- About 400 staff are on FlexPlan (HR number from last year, not rechecked).

## Open questions for the PO
- Finance upgrade value still to confirm for the business case. **PO decision (2 Feb):** proceed; Finance confirms before read-out.
