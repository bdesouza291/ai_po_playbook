---
initiative: flexpay-early-upgrade
stage: backlog
status: APPROVED
version: 3
produced_by: story-writer
upstream: 04-prd.md, 05-metrics-plan.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-11-20 12:00
approved_hash: 3247a69d28435b73
---
# Backlog: Self-serve settlement figure

**Changes in this version (v3, reopened after refinement on 18 Nov)**
- EU2-S1 split into EU2-S1a (link to journey, journey fetches its own figure) and EU2-S1b (refresh on expiry). Team chose this to avoid changing the upgrade journey before spring.
- New EU1-S6: log every generated figure for audit (NFR-03). The Agreement Service doesn't log today.
- EU1-S3: arrears, dispute and support flags come back on the same endpoint.

**Changes in v2 (reopened after test design found AC gaps)**
- EU1-S1: added same-day repeat view scenario (BR-03, `SET.010.030.020`).
- EU1-S5: added keyboard and screen reader scenario for the PDF (`SET.020.010.020`).
- EU2-S1: added scenario for the figure expiring mid-journey at the validity boundary (`SET.020.030.010`).

## Epic map
| Epic | Outcome | PRD requirement IDs | Stories |
|---|---|---|---|
| EU1 Settlement figure self-serve | Mid-contract customers see what they owe without calling | SET.010.010–040, SET.020.010, SET.030.020, SET.030.030, NFR-03, BR-01–05 | EU1-S1 to S6 |
| EU2 Upgrade handoff and support | Customers can act on the figure: upgrade, or get help | SET.020.020, SET.020.030, SET.030.010, SET.040.010 | EU2-S1a, S1b, S2, S3 |
| EU3 Measurement | We can tell if it worked, safely | SET.040.020, SET.040.030 | EU3-S1 to S3 |

## Stories

### EU1-S1: See my settlement figure on the upgrade hub
**As a** mid-contract FlexPlan customer **I want** to see what I'd need to pay to settle my device agreement **so that** I can decide whether to upgrade now.

**Delivers (PRD requirement IDs):** `SET.010.010`, `SET.010.020`, `SET.010.030`

```gherkin
@SET.010.010.010
Scenario: Eligible customer sees the figure
  Given I am logged in with one FlexPlan agreement with 14 months remaining
  And my agreement is not in arrears or dispute
  When I open the upgrade hub
  Then I see a settlement figure card showing the amount, "valid until" date and "14 months left"

@SET.010.010.020
Scenario: Customer near the end of contract
  Given my agreement has 2 months remaining
  When I open the upgrade hub
  Then I see the existing end-of-contract upgrade offer and no settlement card

@SET.010.030.020
Scenario: Same figure on a repeat view the same day
  Given I viewed a figure of £412.50 this morning
  When I return to the upgrade hub this afternoon
  Then I see £412.50 with the same "valid until" date
```
**Notes / rules:** BR-01, BR-03. Card copy from Compliance. Figure from Agreement Service on load (`SET.010.030`).
**Analytics:** settlement_card_requested, settlement_figure_viewed, upgrade_cta_clicked (built in EU3-S1).
**Dependencies:** Agreement Service real-time endpoint (backend lead).
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ (UX lead, sprint 1) · Dependencies known ✔ · Compliance flag: yes

### EU1-S2: See my settlement figure in my account
**As a** mid-contract customer **I want** the same card in my account **so that** I can check what I owe without going into the upgrade hub.

**Delivers (PRD requirement IDs):** `SET.010.010` (account surface)

```gherkin
@SET.010.010.030
Scenario: Card in account
  Given I am an eligible mid-contract customer
  When I open "My device" in my account
  Then I see the same settlement figure card as on the upgrade hub
```
**Notes:** Split from EU1-S1 by interface. Reuses the card component.
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ · Dependencies: EU1-S1 · Compliance flag: yes

### EU1-S3: Clear message when a figure can't be shown
**As a** customer **I want** to understand why I can't see a figure and what to do instead **so that** I'm not stuck.

**Delivers (PRD requirement IDs):** `SET.030.020`, `SET.030.030`

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
```
**Notes:** `SET.030.030`, `SET.030.020`, BR-05. Never show an estimated or cached figure. Arrears, dispute and support flags come back on the same Agreement Service call (refinement 18 Nov).
**Analytics:** settlement_figure_error with reason.
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ · Dependencies: arrears and dispute flags from Agreement Service · Compliance flag: yes

### EU1-S4: Customers with more than one agreement
**As a** customer with two FlexPlan agreements **I want** a figure for each device **so that** I know which one I'm settling.

**Delivers (PRD requirement IDs):** `SET.010.040`

```gherkin
@SET.010.040.010
Scenario: Two agreements
  Given I have an eligible iPhone agreement and an eligible tablet agreement
  When I open the upgrade hub
  Then I see two cards, each labelled with the device name

@SET.010.040.020
Scenario: One eligible, one in arrears
  Given my iPhone agreement is eligible and my tablet agreement is in arrears
  When I open the upgrade hub
  Then I see the iPhone figure and the arrears message for the tablet
```
**Notes:** BR-04. Looks large if device names aren't in the Agreement Service response.
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ · Dependencies known ✔ · Compliance flag: no

### EU1-S5: Download a settlement statement
**As a** customer **I want** a statement I can save **so that** I have a record of the figure and when it expires.

**Delivers (PRD requirement IDs):** `SET.020.010`

```gherkin
@SET.020.010.010
Scenario: Download statement
  Given I can see my settlement figure
  When I select "Download statement"
  Then a PDF downloads showing the amount, validity date, agreement number and device

@SET.020.010.020
Scenario: Accessible statement
  Given I use a screen reader
  When I open the downloaded statement
  Then headings, amount and dates are read in a logical order
  And I can reach "Download statement" by keyboard alone
```
**Notes:** `SET.020.010`, NFR-02. Template content from Compliance.
**Analytics:** settlement_statement_downloaded.
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ · Dependencies: document generation service · Compliance flag: yes

### EU2-S1a: Go from my figure to the upgrade journey
**As a** customer who's seen my figure **I want** to go straight to my upgrade options **so that** I can act on it.

**Delivers (PRD requirement IDs):** `SET.020.020`

```gherkin
@SET.020.020.010
Scenario: Figure matches at order summary
  Given I saw a figure of £412.50 valid until 18 Mar 2026
  When I select "See upgrade options" and reach the order summary on the same day
  Then the summary shows £412.50 to settle my current agreement

@SET.020.020.020
Scenario: Journey can't get a figure
  Given the Agreement Service is unavailable
  When the order summary loads
  Then I can't place the order and I'm shown how to call us
```
**Notes:** `SET.020.020`. The upgrade journey fetches its own figure, so no change to the journey's inputs (refinement split option 2). BR-03 keeps the amount the same on the same day.
**DoR:** INVEST ✔ · AC testable ✔ · Designs: link only · Dependencies: none new · Compliance flag: no

### EU2-S1b: Refresh an expired figure before ordering
**As a** customer whose figure expired while I was deciding **I want** to see the new amount before I order **so that** I'm not surprised.

**Delivers (PRD requirement IDs):** `SET.020.030`

```gherkin
@SET.020.030.010
Scenario: Figure expires mid-journey
  Given my figure is valid until 23:59 today
  And I reach the order summary after midnight
  When the summary loads
  Then a new figure is fetched and shown
  And I see a message that the amount has been updated
```
**Notes:** `SET.020.030`. Next sprint; until then the journey's own fetch covers it, but without the "updated" message.
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ (message) · Dependencies: upgrade journey team · Compliance flag: yes

### EU1-S6: Log every generated figure for audit
**As** Compliance **we want** every settlement figure shown online recorded **so that** we can evidence what a customer was told.

**Delivers (PRD requirement IDs):** `NFR-03`

```gherkin
@NFR-03.010
Scenario: Figure logged
  Given a customer views a figure of £412.50
  When the figure is generated
  Then a record with agreement ID, amount, validity date, channel "web" and timestamp is stored

@NFR-03.020
Scenario: Logging fails
  Given the audit store is unavailable
  When a figure is generated
  Then the figure is not shown and the customer sees the error message from EU1-S3
```
**Notes:** NFR-03. Added after refinement: the Agreement Service doesn't log today. No figure without a record.
**DoR:** INVEST ✔ · AC testable ✔ · Designs: no UI change · Dependencies: backend lead · Compliance flag: yes

### EU2-S2: Help if I'm struggling to pay
**As a** customer who is finding payments hard **I want** to find help from the same page **so that** I don't feel pushed into an upgrade.

**Delivers (PRD requirement IDs):** `SET.030.010`

```gherkin
@SET.030.010.010
Scenario: Help route visible
  Given I can see the settlement card or an ineligible message
  When I look below the figure
  Then I see "Struggling to pay?" linking to the financial support page and phone line

@SET.030.010.020
Scenario: Help route doesn't depend on the figure loading
  Given the Agreement Service is unavailable
  When the card shows an error
  Then the "Struggling to pay?" link is still shown
```
**Notes:** `SET.030.010`. Copy reviewed by Customer Ops and Compliance.
**Analytics:** help_route_clicked.
**DoR:** INVEST ✔ · AC testable ✔ · Designs ✘ · Dependencies: support page URL (Customer Ops lead) · Compliance flag: yes

### EU2-S3: Agents can see the figure a customer viewed
**As a** contact-centre agent **I want** to see that a customer viewed a figure online, the amount and when **so that** I can help them quickly if they call.

**Delivers (PRD requirement IDs):** `SET.040.010`

```gherkin
@SET.040.010.010
Scenario: Figure view recorded
  Given a customer viewed a figure of £412.50 at 10:14
  When an agent opens the customer's CRM record
  Then the contact history shows "Settlement figure viewed online: £412.50, valid until 18 Mar 2026, 10:14"
```
**Notes:** `SET.040.010` (Should). Could slip to the next slice without hurting the test.
**DoR:** INVEST ✔ · AC testable ✔ · Designs: no UI change for customers · Dependencies: CRM team · Compliance flag: no

### EU3-S1: Track the settlement journey
**As the** PO **I want** the events in the tracking plan **so that** we can measure the A/B test.

**Delivers (PRD requirement IDs):** `SET.040.020`

```gherkin
@SET.040.020.010
Scenario: Events fire once with the right properties
  Given I am in the treatment arm
  When I view a figure, download a statement and click "See upgrade options"
  Then settlement_figure_viewed, settlement_statement_downloaded and upgrade_cta_clicked each fire once
  And none of them contains a monetary amount
```
**Notes:** `SET.040.020`, NFR-04. Event list in `05-metrics-plan.md`.
**DoR:** INVEST ✔ · AC testable ✔ · Designs: n/a · Dependencies known ✔ · Compliance flag: no

### EU3-S2: Split customers 50/50 and export assignments
**As the** PO **I want** customers split by ID with assignments joinable to contact and order data **so that** we can compare arms.

**Delivers (PRD requirement IDs):** `SET.040.030`

```gherkin
@SET.040.030.010
Scenario: Stable assignment
  Given a customer is assigned to treatment
  When they return on another device
  Then they are still in treatment

@SET.040.030.020
Scenario: Assignment export
  Given the test is running
  When the daily export runs
  Then the warehouse has customer ID, arm and assignment date for every enrolled customer
```
**Notes:** `SET.040.030`.
**DoR:** INVEST ✔ · AC testable ✔ · Dependencies: data engineering · Compliance flag: no

### EU3-S3: Weekly porting data for the guardrail
**As the** PO **I want** port-outs weekly **so that** the stop rule can be checked during the test.

**Delivers (PRD requirement IDs):** metrics-plan guardrail (no functional requirement; supports the port-out stop rule)

```gherkin
Scenario: Weekly feed
  Given the test is running
  When the weekly porting job runs
  Then port-outs from the past 7 days are in the warehouse by customer ID
```
**Notes:** From the metrics plan. Data story, not customer-facing.
**DoR:** INVEST ✔ · AC testable ✔ · Dependencies: data engineering · Compliance flag: no

## Traceability
<!-- Every Must/Should requirement maps to at least one story. -->
| PRD requirement ID | Requirement | Story IDs | Scenario IDs covered |
|---|---|---|---|
| SET.010.010 | See the settlement figure card | EU1-S1, EU1-S2 | SET.010.010.010, SET.010.010.020, SET.010.010.030 |
| SET.010.020 | Card content | EU1-S1 | (verified within SET.010.010.010) |
| SET.010.030 | Real-time figure | EU1-S1 | SET.010.030.020 |
| SET.010.040 | One card per agreement | EU1-S4 | SET.010.040.010, SET.010.040.020 |
| SET.020.010 | Download a statement | EU1-S5 | SET.020.010.010, SET.020.010.020 |
| SET.020.020 | Into the upgrade journey | EU2-S1a | SET.020.020.010, SET.020.020.020 |
| SET.020.030 | Refresh an expired figure | EU2-S1b | SET.020.030.010 |
| SET.030.010 | Help route | EU2-S2 | SET.030.010.010, SET.030.010.020 |
| SET.030.020 | No figure when ineligible | EU1-S3 | SET.030.020.010, SET.030.020.020 |
| SET.030.030 | Never show a wrong figure | EU1-S3 | SET.030.030.010 |
| SET.040.010 | Agents can see the figure viewed | EU2-S3 | SET.040.010.010 |
| SET.040.020 | Analytics | EU3-S1 | SET.040.020.010 |
| SET.040.030 | A/B flag | EU3-S2 | SET.040.030.010, SET.040.030.020 |
| NFR-01 | Load time | EU1-S3 (timeout), performance test in test scenarios | — |
| NFR-02 | Accessibility | EU1-S5 + DoD checks | SET.020.010.020 |
| NFR-03 | Audit logging | EU1-S6 | NFR-03.010, NFR-03.020 |
| NFR-04 | No PII in analytics | EU3-S1 | SET.040.020.010 |

## Not yet stories (parked)
- Trade-in estimate next to the figure (next slice).
- Device balance in the app (next slice).

## Assumptions the agent made
- Device names are available from the Agreement Service (EU1-S4).
