---
initiative: flexpay-early-upgrade
stage: discovery
status: APPROVED
version: 1
produced_by: discovery-researcher
upstream: 00-brief.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-10-12 16:10
approved_hash: 6692f857329d1eff
---
# Discovery synthesis: Self-serve early upgrade

## Summary
Mid-contract customers who look at upgrading mostly can't get past one blocker: they can't see what they still owe without calling. Five of six interviewees and 19 of 27 relevant app reviews say this. The phone route costs us about £69k a month in settlement calls alone, and the funnel suggests most people don't call at all: only 15% of those who hit the "call us" message click it. A smaller group wants to roll their balance into a new plan, and at least one customer looking at the hub was in financial difficulty, not shopping.

## Sources reviewed
| Source | Type | Size / period | Reliability notes |
|---|---|---|---|
| `interview-notes.md` | Qualitative | 6 customers, Sep 2025 | Small, recruited from non-upgraders only |
| `contact-reasons-q3-2025.csv` | Quantitative | Jul-Sep 2025 | Agent-coded reasons, some miscoding likely |
| `funnel-upgrade-hub-sep-2025.csv` | Quantitative | Sep 2025 | Unique customers, logged-in only |
| `app-store-reviews.md` | Qualitative | 27 of 1,140 reviews, Jul-Sep | Self-selected, skews negative |
| `competitor-desk-research.md` | Desk research | 3 competitors, Oct 2025 | Public pages only |
| `notes-on-data.md` | Analyst notes | Q3 2025 | Upgrade-intent share is agent-recorded |

## Who we heard from
Mid-contract iPhone, Samsung and Pixel customers aged 23-52. **Missing:** customers who did call and then upgraded, store-led customers, and anyone over 60.

## Findings
### F1. Customers can't see what they owe, and that stops the upgrade
- **Evidence:** 5 of 6 interviewees (P1, P2, P3, P4, P6). 19 of 27 relevant app reviews. 27,100 of 30,000 hub visitors saw the "call us for your settlement figure" message (`funnel-upgrade-hub-sep-2025.csv`).
- **Strength:** Strong
- **So what:** The settlement figure is the first gate in the journey, not a detail.

### F2. Most people who hit the "call us" message don't call
- **Evidence:** 4,100 of 27,100 (15%) clicked "call us" (`funnel`). P1 and P6 gave up rather than call.
- **Strength:** Moderate (click is not the same as calling)
- **So what:** The call volume understates the demand. We're losing people silently.

### F3. Mid-contract customers upgrade at about a third of the rate of end-of-contract customers
- **Evidence:** 1,500 of 30,000 (5.0%) mid-contract vs 3,050 of 21,000 (14.5%) in the final three months (`funnel`).
- **Strength:** Strong for the gap; the cause is not proven
- **So what:** Some of the gap is natural (less need), some is likely the blocker in F1.

### F4. The figure alone isn't enough; customers want the net cost of upgrading
- **Evidence:** P2 ("couldn't tell me what my old phone was worth"), P6. Competitor A shows trade-in next to the figure.
- **Strength:** Weak (2 interviews, 1 competitor)
- **So what:** Trade-in alongside the figure may matter, but we need more evidence.

### F5. Some customers want to roll the balance into a new plan
- **Evidence:** P3, P6. Competitor B offers "upgrade any time".
- **Strength:** Weak
- **So what:** Raises affordability and customer-harm questions. Flag for Compliance and Credit Risk.

### F6. Customers in financial difficulty land on the upgrade hub
- **Evidence:** P5.
- **Strength:** Weak (one person), but high severity
- **So what:** A self-serve figure page must give a clear route to help. This is a Consumer Duty consumer support question.

### F7. Phone contact is expensive
- **Evidence:** Q3 average 14,200 settlement calls a month at 7.5 min, 8,100 upgrade enquiries at 11.0 min (`contact-reasons-q3-2025.csv`). At £0.65 a minute that's about £69k and £58k a month (`notes-on-data.md`).
- **Strength:** Strong
- **So what:** Deflection alone has a meaningful value.

## Jobs to be done
| When I... | I want to... | So I can... | Evidence |
|---|---|---|---|
| see a new phone I want | know what I still owe | decide if upgrading now makes sense | F1 |
| am weighing up an upgrade | see the net cost after trade-in | compare it with waiting or switching | F4 |
| am struggling to pay | find out my options | reduce what I pay without getting into trouble | F6 |

## Pain points ranked
| Pain | Frequency | Severity | Who | Evidence |
|---|---|---|---|---|
| Can't see settlement figure online | High | High | All mid-contract | F1, F2 |
| Long call waits | Medium | Medium | Callers | P1, P2 |
| Don't know trade-in value at decision point | Low-Medium | Medium | Upgraders | F4 |
| No help route for those struggling | Low | High | Vulnerable customers | F6 |
| Don't know how far through contract they are | Low | Low | Some | P4 |

## Contradictions and surprises
- We assumed settlement callers mostly want to switch networks. Agent notes say about 70% mention upgrading (`notes-on-data.md`), but that is self-reported on the call.
- P4 would have simply waited if he'd known he was near the end. Showing contract progress could reduce early upgrades for some people. That's a good outcome for them.

## Gaps in the evidence
| Gap | Cheapest way to close it |
|---|---|
| What people do after getting a figure on the phone | CRM pull: settlement calls in Q3 joined to upgrades and port-outs within 30 days |
| Over-60s and store-led customers | Five short calls via store teams |
| Whether trade-in at the decision point changes behaviour | Fake-door test or a question in the next survey |

## Assumptions the agent made
- Funnel "unique customers" are de-duplicated across web and app. Not stated in the file.

## Open questions for the PO
- Do we treat roll-over of balances as in scope, or park it now? **PO decision (12 Oct):** park for this initiative, raise with Credit Risk separately. See `decisions.md`.
- Can we get the CRM join before the opportunity stage? **PO decision (12 Oct):** yes, Ops analyst to supply. Now in `inputs/crm-settlement-call-outcomes-q3-2025.csv`.
