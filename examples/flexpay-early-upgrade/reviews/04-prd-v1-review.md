# Critic review: 04-prd.md v1 (first draft)

**Verdict: Ready with minor fixes**

## Rubric
| Check | Score | Reason | Fix |
|---|---|---|---|
| Traceable | Pass | Goals and baselines match `02-opportunity.md` | - |
| Honest about gaps | Pass | Open questions listed with owners | - |
| Scoped | Pass | Non-goals clear | Add IVR option explicitly, it was in prioritisation |
| Readable | Weak | Section 6 prose is long | Use the flowchart, cut prose to alternative paths |
| Consistent | Pass | Scope matches option A | - |
| No overreach | Pass | Regulatory section asks, doesn't conclude | - |
| Goals with baselines and targets | Pass | | |
| Requirements testable and numbered | Weak | an early draft requirement said the card "loads fast" | Make it a measurable NFR (now NFR-01) |
| NFRs cover accessibility, performance, privacy, audit | Pass | | |
| Failure paths | Fail | No requirement for customers in arrears or dispute | Add a requirement and business rule |

## Spot checks
- 5.0% and 14.5% baselines: match the funnel CSV.
- £4.88 per call: matches 7.5 x £0.65.
- 17.8 contacts per 1,000: 14,200 / 800,000 x 1,000 = 17.75. Rounds correctly.
- 27,100 of 30,000 hit the message: matches funnel.
- 15% clicked call us: 4,100 / 27,100 = 15.1%. OK.

## AI-sounding phrases (v1)
- "a seamless self-serve experience" -> "customers can see the figure online"
- "empower customers to make informed decisions" -> "so customers can decide whether to upgrade, wait or pay off"
- "robust error handling" -> SET.030.030 as written
