---
initiative: flexpay-early-upgrade
stage: handoff
story: EU1-S3
status: DRAFT
version: 1
produced_by: build-spec-writer
upstream: 06-backlog.md, 07-test-scenarios.md, 04-prd.md
owner: Breitner de Souza Eremita
approved_by:
approved_at:
approved_hash:
---
# Build spec: EU1-S3: Clear message when a figure can't be shown

> **For developers and AI coding agents.** This spec is self-contained: you should be able to build the story without opening any other document. Where something is ambiguous or missing, **stop and ask**; don't guess. Requirement and scenario IDs are permanent. Keep them exactly as written.

| | |
|---|---|
| Initiative | `flexpay-early-upgrade` |
| Story | `EU1-S3` |
| Delivers | `SET.030.020`, `SET.030.030` |
| Priority | Must |
| Depends on | EU1-S1 (the settlement card component). Arrears, dispute and support flags from the Agreement Service |
| Questions to | PO: Breitner de Souza Eremita · Tech lead: Backend lead |

## 1. Goal
**As a** customer **I want** to understand why I can't see a figure and what to do instead **so that** I'm not stuck.

The settlement card must never show a wrong, stale or estimated figure, and customers in arrears or in dispute must not be nudged towards an upgrade (PRD §1, §14: "Vulnerable customers pushed to upgrade"). When we can't or shouldn't show a figure, the customer gets a clear reason and a way forward: a call, or the financial support link.

## 2. Requirements delivered

**`SET.030.020` — No figure when ineligible** · Priority: Must
Customers in arrears or with a disputed agreement don't see a figure; they see a message and the support route.

- **Acceptance (BDD)**
  - **`SET.030.020.010` — Agreement in arrears**
    - Given the agreement is in arrears
    - When the customer opens the upgrade hub
    - Then the customer sees no figure and a message offering a call and the financial support link
  - **`SET.030.020.020` — Agreement in dispute**
    - Given the agreement is flagged as in dispute
    - When the customer opens the upgrade hub
    - Then the customer sees no figure and a message to contact the team handling the case

**Rules / notes:** BR-05.

**`SET.030.030` — Never show a wrong figure** · Priority: Must
If the figure can't be produced, the customer sees an explanation and the call option, never a stale or estimated figure.

- **Acceptance (BDD)**
  - **`SET.030.030.010` — Service unavailable**
    - Given the Agreement Service does not respond within the time limit
    - When the card loads
    - Then the customer sees an explanation and the phone number
    - And no amount is shown
  - **`SET.030.030.020` — Malformed amount**
    - Given the Agreement Service returns a missing or malformed amount
    - When the card loads
    - Then the response is treated as an error and no amount is shown

## 3. Acceptance criteria

```gherkin
@SET.030.020.010
Scenario: Agreement in arrears
  Given my agreement is in arrears
  When I open the upgrade hub
  Then I see no figure
  And I see a message explaining I can call us, with the financial support link

@SET.030.030.010
Scenario: Agreement Service unavailable
  Given the Agreement Service does not respond within 3 seconds
  When the card loads
  Then I see "We can't show your figure right now" with the phone number
  And no amount is shown

@SET.030.020.020
Scenario: Agreement in dispute
  Given my agreement is flagged as in dispute
  When I open the upgrade hub
  Then I see no figure and a message to contact the team handling my case

# from PRD
@SET.030.030.020
Scenario: Malformed amount
  Given the Agreement Service returns a missing or malformed amount
  When the card loads
  Then the response is treated as an error and no amount is shown
```

The test plan adds one scenario for these requirements that isn't in Gherkin: `SET.030.030.030` (error analytics). See §6.

## 4. Business rules and constraints
| Ref | Rule or constraint | Applies how |
|---|---|---|
| BR-05 | No figure is shown if the agreement is in arrears, in dispute, or flagged for financial support | All three flags come back on the same Agreement Service call (refinement, 18 Nov). Check them before rendering any amount. Support-flagged: see §8 Q1 |
| NFR-01 | Card shows a figure or an error within 3 seconds for 95% of loads | The timeout for `SET.030.030.010` is 3 seconds. After it, show the error and never wait longer for a figure |
| NFR-02 | Accessible to WCAG 2.2 AA, including the PDF statement | Error and ineligible messages are announced to screen readers and are reachable by keyboard |
| NFR-04 | No settlement figure appears in analytics payloads or URLs (personal financial data) | `settlement_figure_error` carries the reason only, never an amount or agreement number |
| NFR-03 (via EU1-S6) | Every figure generated is logged | Not built here. When EU1-S6's audit store is down, no figure is shown and **this story's** error message is used |

## 5. Out of scope
- The "Struggling to pay?" route below the card: **EU2-S2**. This story only includes the financial support link *inside* the arrears message.
- Several agreements on one account: **EU1-S4** (it reuses this story's arrears message).
- Logging generated figures for audit: **EU1-S6**.
- Refreshing a figure that expires mid-journey: **EU2-S1b**.
- Defining analytics events: **EU3-S1**. This story only fires `settlement_figure_error` with a reason.
- Never show an estimated, cached or "approximate" figure as a fallback, even with a disclaimer (PRD `SET.030.030`).
- Paying the settlement online (PRD non-goal).

## 6. Test intent
Every automated test **must carry its scenario ID** (a Gherkin tag `@<ID>`, a test name starting `<ID> -`, or a trait or attribute), so delivery can be traced back.

| Scenario ID | What it proves | Level | Owner | Test data |
|---|---|---|---|---|
| SET.030.020.010 | Arrears: no figure, call and support message | e2e (stubbed service) | QA | A4 in arrears |
| SET.030.020.020 | Dispute: no figure, case-team message | e2e (stubbed service) | QA | A5 in dispute |
| SET.030.030.010 | Timeout at 3 s shows the error and phone number, no amount | integration | Dev | Stub Agreement Service delay 4 s |
| SET.030.030.020 | Null or malformed amount is treated as an error | unit + integration | Dev | Stub returns null amount |
| SET.030.030.030 | `settlement_figure_error` fires with the correct reason, no amount | e2e analytics | QA | Arrears, dispute and timeout cases |

## 7. Context for the builder
| Area | Pointer |
|---|---|
| Systems involved | Agreement Service (settlement amount, validity date, arrears / dispute / support flags, all on one call). Web account and upgrade hub |
| Existing behaviour to keep | Today every mid-contract customer sees a "call us" message. Keep the phone number and opening hours exactly as they are now |
| Designs | Error and ineligible states pending from the UX lead, sprint 1 |
| Code / modules | Settlement card component shared with EU1-S1, in the web account front end. Error states are added to that component, not to a new one *(added by tech lead, 24 Nov)* |
| Data | Flags read per request; nothing is stored by this story |
| Analytics | `settlement_figure_error` with `reason`. Values as defined in `05-metrics-plan.md`. No amounts, no agreement numbers |

## 8. Open questions
| # | Question | Owner | Blocks build? |
|---|---|---|---|
| 1 | BR-05 also covers agreements **flagged for financial support**, but no scenario covers that case. Same message as arrears? | PO | No. **PO decision, 24 Nov:** show the arrears message. A scenario will be added to the PRD at its next revision |
| 2 | Final wording of the error and ineligible messages | Compliance partner | No. Build with copy keys; Compliance wording lands in sprint 2 |

## 9. Definition of Done
- [ ] Every scenario in §3 and §6 has a test tagged with its scenario ID, and it passes.
- [ ] Nothing outside §2–§3 was built (§5 respected).
- [ ] AC met and demoed to the PO.
- [ ] Accessibility checked to WCAG 2.2 AA.
- [ ] Analytics event verified in the debugger.
- [ ] Release notes line written; feature behind the flag.
- [ ] Build log written and linked from the PR.

---

## Rules for AI coding agents
1. Build only what §2 and §3 describe. Anything else is out of scope (§5), even if it looks helpful.
2. Tag every automated test with its scenario ID from §3. Don't invent new scenario IDs; if you think a scenario is missing, raise it as a question.
3. Don't change requirement wording, acceptance wording, IDs or business rules. If they're wrong or contradictory, stop and ask.
4. If a §7 pointer is `[[TECH LEAD]]` and you need it, or a §8 question blocks your work, stop and ask. Don't guess repo structure, APIs or data.
5. Keep a short **build log** in the PR description: decisions taken, assumptions, anything you couldn't do and why. It feeds the close-out.
6. Never mark the story done or approve your own work. A human reviews it.
