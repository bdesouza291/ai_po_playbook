---
initiative: flexpay-early-upgrade
stage: metrics
status: APPROVED
version: 1
produced_by: metrics-analyst
upstream: 04-prd.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-11-04 10:30
approved_hash: 082cca825fb187d0
---
# Metrics and experiment plan: Self-serve settlement figure

## North star for this initiative
30-day upgrade rate of mid-contract customers who visit the upgrade hub.

## Metric tree
- **Upgrade rate, mid-contract (primary)**
  - Share of mid-contract hub visitors who see a figure
    - Figure card load success rate
  - Share who click through to the upgrade journey
  - Upgrade journey completion rate (existing metric)
- **Settlement contacts per 1,000 agreements (secondary)**
  - Statement downloads
- **Guardrails:** port-out within 30 days of viewing a figure; settlement complaints; help route usage; card error rate

## Metric definitions
| Metric | Type | Definition | Source | Baseline | Target |
|---|---|---|---|---|---|
| Mid-contract upgrade rate | Primary | Customers in arm who placed an upgrade order (any channel) within 30 days of first hub visit / mid-contract customers in arm who visited the hub | Analytics + order data | 5.0% | 6.5% |
| Settlement contact rate | Secondary | Settlement figure contacts from customers in arm / live agreements in arm x 1,000, monthly | Contact centre + flag assignments | 17.8 | -30% vs control |
| Figure view rate | Secondary | Customers who loaded a figure / mid-contract customers in treatment who visited the hub | Analytics | n/a | 70%+ |
| Port-out after viewing | Guardrail | Customers who ported out within 30 days of first figure view (treatment) or settlement call (control) / those customers | CRM + porting data | 9% | No more than 10% |
| Settlement complaints | Guardrail | Complaints coded "settlement" per 10,000 agreements | Complaints system | Track | No increase |
| Card error rate | Guardrail | settlement_figure_error / settlement_card_requested | Analytics | n/a | Under 2% |

## Tracking plan
| Event name | Trigger | Properties | Owner | Story ref |
|---|---|---|---|---|
| settlement_card_requested | Card starts loading | agreement_count, page (hub / account), experiment_arm | Frontend | EU3-S1 |
| settlement_figure_viewed | Figure rendered | months_remaining_band, validity_days, page | Frontend | EU3-S1 |
| settlement_figure_error | Figure can't be shown | reason (unavailable / ineligible_arrears / ineligible_dispute / timeout) | Frontend | EU3-S1 |
| settlement_statement_downloaded | PDF downloaded | page | Frontend | EU3-S1 |
| upgrade_cta_clicked | "See upgrade options" clicked | months_remaining_band | Frontend | EU3-S1 |
| help_route_clicked | "Struggling to pay?" clicked | page | Frontend | EU3-S1 |

No amounts in any event (PRD NFR-04). Months remaining as bands: 3-6, 7-12, 13-24, 25+.

## Experiment design
- **Hypothesis:** H1 from `02-opportunity.md`.
- **Design:** A/B by customer ID with the feature flag. Control sees today's "call us" message.
- **Population and split:** logged-in mid-contract customers visiting the hub or account; 50/50.
- **Primary metric and minimum detectable effect:** upgrade rate, 5.0% to 6.5% (1.5pp absolute).
- **Sample size and duration:** two-proportion test, 95% confidence two-sided, 80% power: about **3,780 customers per arm**. Inputs p1 = 0.05, p2 = 0.065. With about 30,000 eligible visitors a month, that's under two weeks of traffic. Run for **four weeks of enrolment** to cover a full pay cycle, then wait 30 days for the conversion window to close.
- **Guardrails and stop rules:** stop the test if card error rate is over 5% for a day, or port-out in treatment is more than 3pp above control after 2,000 viewers per arm.
- **Decision rule:** ship to 100% if upgrade rate is up with a 95% interval above zero and port-out within guardrail. Iterate if upgrade rate is flat but contacts fall. Roll back if port-out breaches.

## Dashboards and reporting cadence
One test dashboard (arms side by side), daily for the first week, then weekly in sprint review.

## Data gaps and instrumentation stories needed
- Flag assignments must be joinable to contact centre data by customer ID: needs a data story (EU3-S2).
- Porting data is monthly today; need weekly for the guardrail (EU3-S3).

## Assumptions the agent made
- Upgrade orders in stores and telesales can be attributed to customer ID. Confirmed by the Ops analyst in the past, not checked again.

## Open questions for the PO
- Is 30 days the right conversion window? **PO decision (4 Nov):** yes, matches existing reporting.
