---
initiative: {{slug}}
stage: release
status: DRAFT
version: 1
produced_by: release-planner
upstream: 06-backlog.md, 07-test-scenarios.md, 05-metrics-plan.md
owner:
approved_by:
approved_at:
approved_hash:
---
# Release plan: <title>

## What's going out
## Rollout strategy
| Phase | Audience / % | Entry criteria | Exit criteria | Date |
|---|---|---|---|---|

## Feature flags and kill switch

## Reviewed build and independent evidence
| Evidence | Commit / build | Result | Source |
|---|---|---|---|
| Independent review | <commit or build reviewed> | <pass / findings> | <review report> |
| Intended vs implemented | <commit or build reviewed> | <agree / disagreements> | <review report or PRD links> |
| Security review | <commit or build reviewed> | <not requested / pass / findings> | <audit report> |
| Performance review | <commit or build reviewed> | <not requested / pass / findings> | <audit report> |

## Promotion record
- **Candidate build / commit:** <exact reviewed build>
- **Human go / no-go:** <GO / NO-GO / awaiting explicit decision>
- **Decision by:** <name>
- **Decision at:** <date and time>
- **Promoted build / commit:** <exact build serving after promotion>
- **Post-promotion verification:** <smoke test, metrics or link>

## Go / no-go checklist
| Area | Check | Owner | Status |
|---|---|---|---|
| Product | AC met, PO accepted | | |
| Quality | Test scenarios passed, no open P1/P2 | | |
| Data | Events firing, dashboard live | | |
| Ops | Support briefed, scripts and FAQs ready | | |
| Compliance | Sign-off on customer-facing wording | | |
| Comms | Internal and customer comms approved | | |

## Monitoring in the first 72 hours
## Rollback plan and triggers
## Support readiness
## Known issues at launch
## Assumptions the agent made
## Open questions for the PO
