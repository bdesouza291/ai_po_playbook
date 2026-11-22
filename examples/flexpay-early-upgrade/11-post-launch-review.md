---
initiative: flexpay-early-upgrade
stage: postlaunch
status: APPROVED
version: 1
produced_by: metrics-analyst
upstream: 05-metrics-plan.md, 09-release-plan.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2026-04-28 15:30
approved_hash: 965de2a7c940386d
---
# Post-launch review: Self-serve settlement figure

## Summary verdict
It worked, but not as much as we hoped. Mid-contract customers who could see their figure online upgraded at 6.2% against 5.1% in control, a 1.1pp lift that is very unlikely to be chance. That's short of the 6.5% target. Settlement calls fell by a third, port-outs stayed inside the guardrail, and complaints were flat. Ops says customers who've seen their figure now ask about trade-in, which supports the next slice.

## Results vs targets
Source: `inputs/ab-test-results-2026-04.csv`. Calculations run in Python; inputs shown.

| Metric | Baseline (control) | Target | Actual (treatment) | Confidence | Verdict |
|---|---|---|---|---|---|
| 30-day upgrade rate | 5.10% (770 / 15,100) | 6.5% | 6.20% (933 / 15,050) | +1.10pp, 95% CI +0.58 to +1.62pp; z = 4.14, p < 0.001 | Lift is real; target missed |
| Settlement contacts per 1,000 agreements | 17.6 | 30% lower | 11.6 (34% lower) | Monthly rate from contact data; no interval calculated | Met |
| Figure view rate | n/a | 70%+ | Not in the results extract | - | Missing. **PO decision (28 Apr):** analyst to add; doesn't change the verdict |

## Guardrails
| Guardrail | Limit | Control | Treatment | Verdict |
|---|---|---|---|---|
| Port-out within 30 days | No more than 10%, and under +3pp vs control | 9.1% | 9.8% | Within limits, but up 0.7pp. Keep watching |
| Settlement complaints | No increase | 41 | 39 | OK |
| Card error rate | Under 2% | n/a | 1.2% | OK |

## What surprised us
- Port-out went up a little, not down. Some customers do use the figure to leave. It's inside the guardrail, and those customers may have left anyway after calling.
- 11 calls where the online figure didn't match the agent's figure, all caused by expiry at midnight before EU2-S1b shipped (`inputs/ops-feedback-2026-04.md`). No wrong figures.

## Customer and ops feedback
- Callers in treatment already know their figure and want trade-in values.
- 1,240 help route clicks; no change in financial support waiting times.

## Hypotheses
| ID | Verdict | Evidence |
|---|---|---|
| H1 Self-serve figure lifts upgrades | Validated (smaller than targeted) | +1.10pp, significant |
| H2 Fewer settlement calls | Validated | 34% lower |
| H3 Won't drive more pay-off-and-leave | Partly: small rise inside guardrail | 9.8% vs 9.1% |
| H4 Trade-in adds further lift | Not tested yet | Ops feedback suggests demand |

## Recommendation
**Scale to 100% and move to the next slice.** The PO decides.
- Roll out to all mid-contract customers.
- Next slice: trade-in estimate next to the figure (H4), as its own A/B test.
- Ship EU2-S1b (refresh with message) before 100%.
- Keep the port-out guardrail on the dashboard for three months.

At 1.1pp on 30,000 visitors a month and the assumed £180 value, plus 34% fewer settlement calls, that's roughly £0.71m + £0.28m = **£1.0m a year**, between the low and likely cases in `02-opportunity.md`. The upgrade value is still Finance's to confirm.

## Follow-up backlog items
- EU2-S1b before full rollout.
- Trade-in estimate next to the figure (new initiative brief).
- Device balance in the app.
- Port-out deep dive: who leaves after viewing, and what offer they saw.

## What we'd do differently
- Ship the expiry refresh with the MVP; the 11 mismatched calls were avoidable.
- Ask for the view-rate metric in the results extract up front.

## Assumptions the agent made
- Contact rates are monthly averages across the test period, not per-customer, so no significance test was run on them.
