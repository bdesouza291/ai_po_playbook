---
initiative: flexpay-early-upgrade
stage: opportunity
status: APPROVED
version: 1
produced_by: opportunity-framer
upstream: 01-discovery.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-10-14 17:00
approved_hash: 370655a4ab9b3c11
---
# Opportunity: Self-serve early upgrade

## Problem statement
Mid-contract FlexPlan customers who want a new phone can't find out what they still owe without calling us, so most give up or buy elsewhere, and the ones who do call cost us about £69k a month in settlement calls. We know because 27,100 of 30,000 mid-contract hub visitors hit the "call us" message in September, only 15% clicked it, and 5 of 6 interviewees named the figure as the blocker (`01-discovery.md` F1-F3, F7).

## Desired outcome
- **Customer outcome:** a mid-contract customer can see what they owe and decide whether to upgrade, wait or pay off, without calling.
- **Business outcome:** more mid-contract customers upgrade with us; fewer settlement calls.
- **Guardrails (must not get worse):** port-outs within 30 days of seeing a figure; complaints about settlement; bad debt on new agreements; support for customers in difficulty.

## Opportunity sizing
| Input | Value | Known / Assumed | Source |
|---|---|---|---|
| Unique mid-contract hub visitors a month | 30,000 | Known | `funnel-upgrade-hub-sep-2025.csv` |
| Baseline 30-day upgrade rate, mid-contract | 5.0% | Known | same (1,500 / 30,000) |
| Settlement calls a month | 14,200 | Known | `contact-reasons-q3-2025.csv` (Q3 average) |
| Cost of a settlement call | £4.88 (7.5 min x £0.65) | Known | contact reasons + `notes-on-data.md` |
| Uplift in upgrade rate (pp) | 0.5 / 1.5 / 2.5 | **Assumed** | Gap to final-3-months rate is 9.5pp; we assume we close a small part |
| Value of an incremental upgrade, 12 months | £150 / £180 / £210 | **Assumed** | Finance to confirm: airtime margin uplift plus retention |
| Share of settlement calls deflected | 25% / 40% / 55% | **Assumed** | Competitor A and B offer self-serve; no internal benchmark |

| Scenario | Calculation | Annual value |
|---|---|---|
| Low | (30,000 x 0.5% x £150 x 12) + (14,200 x 25% x £4.88 x 12) = £270,000 + £207,675 | **£0.48m** |
| Likely | (30,000 x 1.5% x £180 x 12) + (14,200 x 40% x £4.88 x 12) = £972,000 + £332,280 | **£1.30m** |
| High | (30,000 x 2.5% x £210 x 12) + (14,200 x 55% x £4.88 x 12) = £1,890,000 + £456,885 | **£2.35m** |

Call cost uses the unrounded £4.875. Deflection value is cost avoided, not cash saved, unless the contact centre reduces hours.

## Opportunity tree
- **Outcome:** more mid-contract customers upgrade with us, fewer settlement calls
  - Opportunity: customers can't see what they owe
    - Show settlement figure self-serve, with a downloadable statement
    - Show balance and months remaining in app and web account
    - SMS a settlement figure from the IVR (non-digital option)
  - Opportunity: customers can't see the net cost of upgrading
    - Trade-in estimate shown next to the figure
    - "Cost to upgrade today" summary
  - Opportunity: customers in difficulty land in a sales journey
    - Help route on the same page, to the financial support team
  - Opportunity: customers want to spread the remaining balance
    - Roll-over into new agreement (**parked**, see `decisions.md`)

## Hypotheses
| ID | We believe that... | will result in... | We'll know when... | Riskiest? |
|---|---|---|---|---|
| H1 | showing the settlement figure online | more mid-contract customers upgrading with us | 30-day upgrade rate rises from 5.0% toward 6.5% in an A/B test | Yes |
| H2 | showing the settlement figure online | fewer settlement calls | settlement contacts per 1,000 agreements fall by at least 30% in the test group | |
| H3 | showing the figure online | will not drive more customers to pay off and leave | port-out within 30 days of seeing a figure stays within 1pp of the call-route baseline (9%) | Yes |
| H4 | adding trade-in value next to the figure | a further lift in upgrades | upgrade rate in a trade-in cell beats figure-only | |

## Riskiest assumptions and cheapest tests
| Assumption | Type | Test | Cost | Signal |
|---|---|---|---|---|
| People who see the figure upgrade rather than leave (H1, H3) | Value / viability | CRM join already shows call-route outcomes: 21% upgrade, 9% pay off and port out (`crm-settlement-call-outcomes-q3-2025.csv`). Use as the baseline; A/B test the online route | Low | Port-out share in test vs 9% |
| Agreement Service can produce a figure in real time | Feasibility | 30-minute spike with backend lead | Very low | Yes / no plus latency |
| Customers understand the figure and its validity | Usability | 5 moderated tests of the figure page | Low | 4 of 5 can explain what they'd pay and by when |

## Regulatory and customer-harm considerations
Questions for Compliance (from `context/regulatory-notes.md`):
- What must a self-serve settlement figure show, and how long can it be valid for?
- Does a downloadable statement meet the requirement to provide a settlement statement on request, or is a separate process still needed?
- How do we evidence Consumer Duty consumer understanding for the figure page?
- What does a help route for customers in difficulty need to include (F6)?

## Assumptions the agent made
- Value per incremental upgrade is a placeholder until Finance confirms.
- The 70% upgrade intent among callers (`notes-on-data.md`) is not used in sizing because it is self-reported.

## Open questions for the PO
- Finance to confirm upgrade value range. **PO decision (14 Oct):** use £150-£210 for now, flagged as assumed; Finance confirmation is a PRD open question.
