---
initiative: flexpay-early-upgrade
stage: test
status: APPROVED
version: 2
produced_by: qa-scenario-designer
upstream: 06-backlog.md
owner: Breitner de Souza Eremita
approved_by: Breitner de Souza Eremita
approved_at: 2025-11-21 10:00
approved_hash: 0fbbf7e73174ecec
---
# Test scenarios: Self-serve settlement figure

**Changes in this version (v2, after backlog v3)**
- `SET.020.020.010` maps to EU2-S1a; `SET.020.030.010` and `SET.020.020.020` to EU2-S1b / EU2-S1a.
- Added `NFR-03.010` and `NFR-03.020` for EU1-S6 audit logging.

## Scope and approach
Functional scenarios per story, plus accessibility, analytics, performance and audit. Scenario IDs reuse the PRD/backlog stable IDs where one exists; QA-only scenarios extend the same requirement ID with a fresh `.<SCN>`. Automated where the team's framework supports it; accessibility and PDF checks are manual.

## Coverage summary
| Story | Happy | Negative | Edge | Accessibility | Analytics | Total |
|---|---|---|---|---|---|---|
| EU1-S1 | 1 | 1 | 2 | 1 | 1 | 6 |
| EU1-S2 | 1 | 0 | 0 | 0 | 0 | 1 |
| EU1-S3 | 0 | 3 | 1 | 0 | 1 | 5 |
| EU1-S4 | 1 | 1 | 0 | 0 | 0 | 2 |
| EU1-S5 | 1 | 0 | 0 | 2 | 1 | 4 |
| EU1-S6 | 1 | 1 | 0 | 0 | 0 | 2 |
| EU2-S1a | 1 | 1 | 0 | 0 | 0 | 2 |
| EU2-S1b | 0 | 0 | 1 | 0 | 0 | 1 |
| EU2-S2 | 1 | 1 | 0 | 1 | 1 | 4 |
| EU2-S3 | 1 | 0 | 0 | 0 | 0 | 1 |
| EU3-S1 | 0 | 1 | 0 | 0 | 0 | 1 |
| EU3-S2 | 2 | 0 | 0 | 0 | 0 | 2 |

## Scenarios
| Scenario ID | Requirement ID | Story | Type | Scenario | Preconditions / data | Expected result | Priority |
|---|---|---|---|---|---|---|---|
| SET.010.010.010 | SET.010.010 | EU1-S1 | Happy | Eligible customer sees figure | Agreement A1, 14 months left, no flags | Card with amount, valid-until date, "14 months left" | P1 |
| SET.010.010.020 | SET.010.010 | EU1-S1 | Edge | Exactly 3 months remaining | A2, 3 full months left | No card; end-of-contract offer (BR-01 boundary) | P1 |
| SET.010.010.040 | SET.010.010 | EU1-S1 | Edge | 4 months remaining | A3 | Card shown | P2 |
| SET.010.030.020 | SET.010.030 | EU1-S1 | Negative | Same-day repeat view | A1 viewed at 09:00 | Same amount and date at 15:00 (BR-03) | P2 |
| SET.010.020.020 | SET.010.020 | EU1-S1 | Accessibility | Card read by screen reader | A1, NVDA and VoiceOver | Amount, date, months read in order; contrast AA | P1 |
| SET.040.020.020 | SET.040.020 | EU1-S1 | Analytics | View events | A1, treatment arm | requested + viewed fire once; no amount in payload | P1 |
| SET.010.010.030 | SET.010.010 | EU1-S2 | Happy | Card in account | A1 | Same card as hub | P2 |
| SET.030.020.010 | SET.030.020 | EU1-S3 | Negative | Arrears | A4 in arrears | No figure; message and support link | P1 |
| SET.030.020.020 | SET.030.020 | EU1-S3 | Negative | Dispute | A5 in dispute | No figure; case team message | P1 |
| SET.030.030.010 | SET.030.030 | EU1-S3 | Negative | Timeout | Stub Agreement Service delay 4s | Error message with phone number; no amount | P1 |
| SET.030.030.020 | SET.030.030 | EU1-S3 | Edge | Service returns malformed amount | Stub returns null amount | Treated as error, no amount shown | P1 |
| SET.030.030.030 | SET.030.030 | EU1-S3 | Analytics | Error events | arrears / dispute / timeout cases | settlement_figure_error with correct reason | P2 |
| SET.010.040.010 | SET.010.040 | EU1-S4 | Happy | Two eligible agreements | A1 + tablet T1 | Two labelled cards | P2 |
| SET.010.040.020 | SET.010.040 | EU1-S4 | Negative | One eligible, one arrears | A1 + T2 in arrears | One card, one arrears message | P2 |
| SET.020.010.010 | SET.020.010 | EU1-S5 | Happy | Download PDF | A1 | PDF has amount, validity, agreement number, device | P1 |
| SET.020.010.020 | SET.020.010 | EU1-S5 | Accessibility | PDF tagged | A1 | Tagged PDF, logical reading order | P1 |
| SET.020.010.030 | SET.020.010 | EU1-S5 | Accessibility | Keyboard only | A1 | Download reachable and operable by keyboard | P1 |
| SET.040.020.030 | SET.040.020 | EU1-S5 | Analytics | Download event | A1 | Fires once per download | P3 |
| SET.020.020.010 | SET.020.020 | EU2-S1a | Happy | Figure carried to summary | A1 | Same amount at order summary | P1 |
| SET.020.030.010 | SET.020.030 | EU2-S1b | Edge | Expiry at midnight | A1 valid until 23:59, clock moved to 00:01 | New figure fetched, update message shown | P1 |
| SET.020.020.020 | SET.020.020 | EU2-S1a | Negative | Service down at order summary | Stub down | Order blocked; call option shown | P1 |
| SET.030.010.010 | SET.030.010 | EU2-S2 | Happy | Help link shown | A1 | "Struggling to pay?" present below figure | P1 |
| SET.030.010.020 | SET.030.010 | EU2-S2 | Negative | Help link on error | As timeout case | Help link still present | P1 |
| SET.030.010.030 | SET.030.010 | EU2-S2 | Accessibility | Help link name | A1 | Link text makes sense out of context | P2 |
| SET.040.020.040 | SET.040.020 | EU2-S2 | Analytics | Help click | A1 | help_route_clicked fires | P2 |
| SET.040.010.010 | SET.040.010 | EU2-S3 | Happy | CRM record | A1 viewed at 10:14 | Contact history entry with amount and time | P2 |
| SET.040.020.010 | SET.040.020 | EU3-S1 | Negative | No PII in events | All events | No amounts, no agreement numbers | P1 |
| SET.040.030.010 | SET.040.030 | EU3-S2 | Happy | Stable assignment | Customer C1 on two browsers | Same arm | P1 |
| SET.040.030.020 | SET.040.030 | EU3-S2 | Happy | Daily export | Test running | Warehouse rows for all enrolled | P2 |
| NFR-03.010 | NFR-03 | EU1-S6 | Happy | Figure logged | A1 | Audit record with agreement ID, amount, validity, channel, timestamp | P1 |
| NFR-03.020 | NFR-03 | EU1-S6 | Negative | Audit store down | Stub audit store failure | No figure shown; SET.030.030 error message | P1 |
| NFR-01.010 | NFR-01 | All | Performance | Load time | 95th percentile on 4G profile | Figure or error within 3 seconds | P1 |

## Traceability and coverage
<!-- Every PRD requirement has at least one scenario here. -->
| PRD requirement ID | Scenarios covering it | Covered? |
|---|---|---|
| SET.010.010 | SET.010.010.010, .020, .030, .040 | Yes |
| SET.010.020 | SET.010.020.020 (and within SET.010.010.010) | Yes |
| SET.010.030 | SET.010.030.020 | Yes |
| SET.010.040 | SET.010.040.010, .020 | Yes |
| SET.020.010 | SET.020.010.010, .020, .030 | Yes |
| SET.020.020 | SET.020.020.010, .020 | Yes |
| SET.020.030 | SET.020.030.010 | Yes |
| SET.030.010 | SET.030.010.010, .020, .030 | Yes |
| SET.030.020 | SET.030.020.010, .020 | Yes |
| SET.030.030 | SET.030.030.010, .020, .030 | Yes |
| SET.040.010 | SET.040.010.010 | Yes |
| SET.040.020 | SET.040.020.010, .020, .030, .040 | Yes |
| SET.040.030 | SET.040.030.010, .020 | Yes |
| NFR-01 | NFR-01.010 | Yes |
| NFR-02 | SET.020.010.020 + DoD checks | Yes |
| NFR-03 | NFR-03.010, .020 | Yes |
| NFR-04 | SET.040.020.010 | Yes |

## Test data needed
Agreements A1-A5 and T1-T2 in the test environment with the flags above; an Agreement Service stub that can delay, fail and return malformed data; a clock control for the expiry test (SET.020.030.010).

## Regulatory and audit checks
- Card and PDF wording matches the Compliance-approved copy word for word.
- Every figure generated is logged (NFR-03): NFR-03.010, NFR-03.020.

## Non-functional checks
NFR-01.010, accessibility as above, mobile viewport layout at 320px.

## Gaps found in the acceptance criteria
Raised against backlog v1 and fixed in backlog v2:
- EU1-S1 had no scenario for BR-03 (same-day repeat view). Now `SET.010.030.020`.
- EU1-S5 had no accessibility scenario for the PDF. Now `SET.020.010.020`.
- EU2-S1 didn't cover the validity boundary. Now `SET.020.030.010`.

Raised in v1 and fixed in backlog v3:
- NFR-03 audit logging had no story. Now EU1-S6 (`NFR-03.010`, `NFR-03.020`).

## Assumptions the agent made
- The team can stub the Agreement Service in the test environment.
