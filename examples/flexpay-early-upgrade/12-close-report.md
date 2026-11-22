---
initiative: flexpay-early-upgrade
stage: close
status: DRAFT
version: 1
produced_by: close-analyst
upstream: 06-backlog.md, 07-test-scenarios.md, 04-prd.md
owner: Breitner de Souza Eremita
approved_by:
approved_at:
approved_hash:
---
# Close report: Self-serve settlement figure (early upgrade MVP)

| | |
|---|---|
| Evidence checked | `inputs/ci-test-results-2026-05-01.xml` (CI, main branch, 1 May 2026) and `inputs/manual-test-log-2026-02.csv` (QA manual checks, 10–11 Feb 2026), via `pdlc.py trace --evidence` |
| Delivery window | PR #201 merged 9 Jan 2026 to PR #210 merged 5 Feb 2026 (`inputs/pr-build-logs.md`) |
| Verdict | **Close with follow-ups** |

## 1. Summary
The MVP shipped as the release plan scoped it. 11 of the 12 Must requirements are Implemented (full), with passing automated or manual tests for every scenario. One Must requirement, `SET.020.030` (refresh an expired figure), and one Should, `SET.040.010` (CRM record), have no evidence because their stories, EU2-S1b and EU2-S3, were moved behind the A/B test and haven't been built. The post-launch review already asks for EU2-S1b before the 100% rollout. Close the MVP now, with those two as owned follow-ups.

## 2. Delivery against the PRD
| Requirement | Priority | Passing | Implementation | Notes |
|---|---|---|---|---|
| SET.010.010 | Must | 4/4 | Implemented (full) | |
| SET.010.020 | Must | 2/2 | Implemented (full) | `.010` passes as a dev test (PR #201); not in the test plan, see §4 |
| SET.010.030 | Must | 2/2 | Implemented (full) | `.010` passes as a dev test (PR #201); not in the test plan, see §4 |
| SET.010.040 | Must | 2/2 | Implemented (full) | |
| SET.020.010 | Must | 3/3 | Implemented (full) | Accessibility scenarios passed manually |
| SET.020.020 | Must | 2/2 | Implemented (full) | |
| SET.020.030 | Must | 0/1 | No evidence | EU2-S1b not built; moved behind the A/B test (`09-release-plan.md`) |
| SET.030.010 | Must | 3/3 | Implemented (full) | `.030` passed manually |
| SET.030.020 | Must | 2/2 | Implemented (full) | |
| SET.030.030 | Must | 3/3 | Implemented (full) | `.030` skipped in CI, passed manually (PR #203) |
| SET.040.010 | Should | 0/1 | No evidence | EU2-S3 not built |
| SET.040.020 | Must | 4/4 | Implemented (full) | |
| SET.040.030 | Must | 2/2 | Implemented (full) | |

Script verdict: NOT CLOSED, because `SET.020.030` is not fully implemented. This report's verdict is *Close with follow-ups* because that gap is known, owned and planned (§5).

## 3. Scenarios without a passing test
| Scenario ID | Requirement | Evidence status | Why | Action |
|---|---|---|---|---|
| SET.020.030.010 | SET.020.030 | MISSING | Not built: EU2-S1b deferred behind the A/B test | Follow-up EU2-S1b (already in the backlog), before 100% rollout |
| SET.040.010.010 | SET.040.010 | MISSING | Not built: EU2-S3 deferred | Follow-up EU2-S3, or a descope decision (§6) |

## 4. Drift: what shipped differs from the spec
| # | What the spec says | What shipped | Source | Proposed action |
|---|---|---|---|---|
| 1 | Release plan: until EU2-S1b ships "the journey fetches its own figure, so there's no expiry gap" | 11 calls where the customer's online figure didn't match the agent's, all after midnight expiry | `inputs/ops-feedback-2026-04.md`; `11-post-launch-review.md` | No product change: this is the EU2-S1b gap. Record in `decisions.md` that the interim assumption was wrong |
| 2 | PRD `SET.030.030.010`: "does not respond within the time limit" | Timeout of 3 s, per the story and NFR-01 | PR #203 build log | `/reopen` the PRD at its next revision to say "within 3 seconds" |
| 3 | BR-05 covers agreements "flagged for financial support", but no PRD scenario does | Support-flagged agreements get the arrears message (build spec §8 Q1); a test exists **with no scenario ID** | `handoff/EU1-S3.md`; PR #203 | `/reopen` the PRD to add `SET.030.020.030`, then tag the existing test with it |
| 4 | Test plan (`07-test-scenarios.md`) has no rows for PRD scenarios `SET.010.020.010` and `SET.010.030.010` | Dev tests exist and pass | PR #201; `pdlc.py trace` warnings | Add both rows at the test plan's next revision |

## 5. Follow-up stories (drafts)

### EU2-S1b: Refresh an expired figure before ordering *(existing story, still open)*
**Delivers (PRD requirement IDs):** `SET.020.030`
**Why:** the only Must gap (§3), and the cause of the 11 mismatched calls (§4 #1). Already specified in the backlog; build before the 100% rollout, as the post-launch review recommends.
```gherkin
@SET.020.030.010
Scenario: Figure expires mid-journey
  Given my figure is valid until 23:59 today
  And I reach the order summary after midnight
  When the summary loads
  Then a new figure is fetched and shown
  And I see a message that the amount has been updated
```

### EU1-S7: Support-flagged agreements show the arrears message *(new)*
**Delivers (PRD requirement IDs):** `SET.030.020` (once `SET.030.020.030` is added, §4 #3)
**Why:** the behaviour shipped and works, but it isn't specified or traceable. This story is only the PRD scenario plus tagging the existing test; no new build.
```gherkin
@SET.030.020.030
Scenario: Agreement flagged for financial support
  Given my agreement is flagged for financial support
  When I open the upgrade hub
  Then I see no figure
  And I see a message explaining I can call us, with the financial support link
```

## 6. Descope decisions to record
| Requirement | Decision needed | Owner |
|---|---|---|
| SET.040.010 (Should) | Build EU2-S3 (agents see the figure a customer viewed) in the next slice, or descope it? The release plan's interim workaround (agents generate a new figure) has run since February with no reported harm | [[OPEN]] PO, with the Customer Ops lead |

## 7. Evidence quality
- **Strong:** CI results are JUnit XML with a pass status for 24 tagged scenarios. Manual checks are dated, name the tool and the tester, and cover the four accessibility scenarios plus the analytics check that CI skips.
- **One untraceable test:** the support-flag test in PR #203 has no scenario ID, so no tool can count it (§4 #3).
- **One CI skip:** `SET.030.030.030` is skipped in headless CI and rests on a single manual check from 11 Feb. Worth automating once the tag manager can load in CI.
- The CI run is from 1 May, after the A/B test. The manual checks are from February and haven't been repeated since.

## Assumptions the agent made
- The scope in `09-release-plan.md` is what was intended to ship. Nothing outside it was expected.

## Open questions for the PO
- [[OPEN]] EU2-S3: build or descope (§6)?
