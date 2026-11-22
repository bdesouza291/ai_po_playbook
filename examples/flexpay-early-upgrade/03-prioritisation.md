---
initiative: flexpay-early-upgrade
stage: prioritisation
status: APPROVED
version: 1
produced_by: prioritisation-analyst
upstream: 02-opportunity.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-10-16 15:20
approved_hash: 7cea59638e122335
---
# Solution options and prioritisation: Self-serve early upgrade

## Options considered
| ID | Option | What it involves | Main risk |
|---|---|---|---|
| A | Self-serve settlement figure | Figure on web account and upgrade hub, downloadable statement, months remaining, link into the existing upgrade journey, help route for customers in difficulty | Some customers pay off and leave (H3) |
| B | A plus trade-in estimate | As A, plus trade-in estimate from the partner API and a "cost to upgrade today" summary | Trade-in quotes change after inspection; customer disappointment |
| C | B plus roll-over of balance | Remaining balance added to a new FlexPlan agreement | Affordability and customer-harm risk; Credit Decisioning change (6-week lead time) |
| D | IVR text-back only | Customers who call get an SMS figure without talking to an agent | Doesn't fix the online drop-off (F2) |
| E | Do nothing now, revisit after spring | No build | Lose the spring launch window |

## Scoring
Method: RICE (team default), with confidence from discovery evidence strength. Reach is mid-contract hub visitors a quarter (90,000) unless noted. Impact on a 0.25-3 scale. Effort is a T-shirt placeholder, **to be estimated by the team**.

| Option | Reach (qtr) | Impact | Confidence | Effort (T-shirt) | Score | Notes |
|---|---|---|---|---|---|---|
| A | 90,000 | 2 | 80% (F1 Strong) | M (5) | 28,800 | Most evidence, fixes the main blocker |
| B | 90,000 | 2.5 | 50% (F4 Weak) | L (8) | 14,063 | Adds partner integration and quote-change edge cases |
| C | 90,000 | 3 | 30% (F5 Weak) | XL (13) | 6,231 | Score ignores harm risk; see below |
| D | 42,600 callers | 1 | 80% | S (3) | 11,360 | Cheap but only helps people who already call |
| E | 0 | 0 | - | - | 0 | Baseline |

## Trade-offs in plain words
- A fixes the problem most people actually have, and we can test it cleanly.
- B might add more, but the evidence is two interviews and one competitor. Better as a follow-on test once A is live.
- C scores well on impact but carries the most risk for customers who are already stretched. Score does not override harm. Needs Credit Risk and Compliance before it's even an option.
- D is cheap and helps phone customers, including those not online. Worth doing alongside, but it doesn't touch the 85% who never call.

## Recommendation
- **Recommended:** A as the MVP, with B as the next slice if H1 is supported.
- **Why:** strongest evidence, lowest risk, testable before the spring launches.
- **What we'd give up:** the possible extra lift from trade-in in the first release.
- **What would change my mind:** if usability testing shows customers can't act on a figure without knowing their trade-in value, move trade-in into the MVP.

## Proposed slicing
| Release slice | Contents | Outcome it tests |
|---|---|---|
| MVP | Option A on web, A/B tested | H1, H2, H3 |
| Next | Trade-in estimate next to the figure (B); balance in app | H4 |
| Later / not now | IVR text-back (D) to Ops backlog; roll-over (C) parked pending Credit Risk | - |

## Assumptions the agent made
- 42,600 for D is the Q3 settlement call total (13,900 + 14,600 + 14,100).

## Open questions for the PO
- Should D go to the Ops team's backlog rather than ours? **PO decision (16 Oct):** yes, raised with Customer Ops lead.
