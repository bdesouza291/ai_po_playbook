# Product context

> **Swap this file first when you join a new company.** Every agent reads it before drafting.
> The content below is a **fictional** product used for the worked example. Numbers are illustrative.

## Company and product
- **Company:** Northwind Mobile, a UK mobile network operator (fictional).
- **Product:** FlexPlan, handset financing. Customers spread the cost of a phone over 12, 24 or 36 months on a regulated credit agreement, alongside a separate airtime plan.
- **Channels:** responsive web (about 70% of traffic on mobile viewports), native app (account management only), retail stores, telesales.
- **Scale:** about 800,000 live FlexPlan agreements; around 20,000 new agreements a month.

## Customers
| Segment | Share | What they care about |
|---|---|---|
| Upgraders (existing customers on a new device) | ~55% | Speed, not repeating checks, knowing what they still owe |
| New-to-network | ~35% | Price, approval certainty, trust |
| Credit-thin / younger customers | ~10% | Being accepted at all, low upfront cost |

Vulnerable customers are present in every segment, not a segment of their own.

## Business model
- Revenue from airtime plans; FlexPlan itself is priced at 0% APR. The operator funds the credit through a captive finance arm.
- Key business levers: new-device conversion, early upgrade volume, bad debt rate, cost to serve (calls and store time), churn at end of contract.

## Current strategy (this year)
1. Shift routine servicing contacts to self-serve.
2. Grow upgrade volume among existing customers.
3. Meet Consumer Duty outcomes evidence requirements for every customer journey.

## Tech landscape (names only; the team owns design)
- Web and app front ends share the same backend APIs.
- **Agreement Service** holds credit agreements and balances.
- **Credit Decisioning** (third-party engine plus credit reference agency checks).
- **Trade-in partner API** for device valuations.
- **CRM** for contact history; **Contact centre platform** with contact reason codes.
- Analytics: product analytics tool for funnels, warehouse for finance data.

## Team
See `team-and-ways-of-working.md`.

## Known constraints
- Any customer-facing wording about credit, balances or settlement needs compliance review.
- Two-week release train; feature flags available on web, app releases go through store review.
- Credit Decisioning changes have a six-week lead time with the vendor.
