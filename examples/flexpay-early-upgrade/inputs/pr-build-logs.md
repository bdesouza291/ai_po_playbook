# PR build logs (fictional extracts)

Copied from the "Build log" section of each PR description, sprints 1–4. Flag: `settlement_selfserve`.

| PR | Story | Merged | Build log |
|---|---|---|---|
| #201 | EU1-S1 | 2026-01-09 | Card component and eligibility (BR-01). Also added dev tests for two PRD scenarios the test plan doesn't list: `SET.010.020.010` (card content) and `SET.010.030.010` (figure requested on load). |
| #202 | EU1-S2 | 2026-01-12 | Reused the card in My device. No new logic. |
| #203 | EU1-S3 | 2026-01-16 | Built from `handoff/EU1-S3.md` v1. Timeout set to 3 s: the story and NFR-01 say 3 seconds, the PRD scenario `SET.030.030.010` says "the time limit". Support-flagged agreements get the arrears message (spec §8 Q1); test added but **it has no scenario ID** because the PRD has none yet. `SET.030.030.030` can't run in headless CI (tag manager not loaded), so it's skipped there and checked by hand. |
| #204 | EU1-S4 | 2026-01-20 | One card per agreement, labelled with the device name from the Agreement Service. |
| #205 | EU1-S5 | 2026-01-23 | Statement PDF via the document generation service. Accessibility checked manually by QA. |
| #206 | EU2-S1a | 2026-01-27 | Link to the upgrade journey. The journey fetches its own figure; no change to its inputs. |
| #207 | EU2-S2 | 2026-01-28 | "Struggling to pay?" route below the card, shown on error too. |
| #208 | EU3-S1 | 2026-01-30 | Tracking plan events. No amounts in payloads. |
| #209 | EU1-S6 | 2026-02-03 | Audit log of every generated figure (NFR-03). No figure without a record. |
| #210 | EU3-S2, EU3-S3 | 2026-02-05 | 50/50 assignment, daily export, weekly porting feed. |

**Not started:** EU2-S1b (refresh on expiry) and EU2-S3 (CRM record). Both were moved behind the A/B test in the release plan, and are still open on 1 May 2026.
