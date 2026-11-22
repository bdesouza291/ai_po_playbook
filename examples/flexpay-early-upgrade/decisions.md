# Product decisions - flexpay-early-upgrade

| Date | Decision | Why | Who | Source |
|---|---|---|---|---|
| 12 Oct | Park roll-over of balances into a new agreement | Customer-harm and affordability risk; needs Credit Risk and Compliance first | PO | `01-discovery.md` F5 |
| 12 Oct | Get CRM join of settlement callers to outcomes before sizing | Need a baseline for the "pay off and leave" risk | PO | `01-discovery.md` gaps |
| 14 Oct | Use £150-£210 upgrade value as assumed range | Finance can't confirm before PRD | PO | `02-opportunity.md` |
| 16 Oct | MVP is option A; trade-in is the next slice | Strongest evidence, testable before spring | PO | `03-prioritisation.md` |
| 16 Oct | IVR text-back goes to Customer Ops backlog | Helps callers but not the 85% who never call | PO with Customer Ops lead | `03-prioritisation.md` |
| 30 Oct | Help route for customers in difficulty is a Must | Consumer Duty consumer support; F6 | PO | PRD v2 |
| 4 Nov | 30-day conversion window | Matches existing reporting | PO | `05-metrics-plan.md` |
| 18 Nov | Split EU2-S1; MVP links to journey which fetches its own figure | Avoids change to upgrade journey team's code before spring | PO + team | Refinement 18 Nov |
| 18 Nov | Add audit logging story (EU1-S6) | Agreement Service doesn't log figures today | PO | Refinement 18 Nov |
