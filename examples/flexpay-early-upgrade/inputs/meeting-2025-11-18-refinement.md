# Refinement session notes, 18 Nov 2025 (fictional)

Attendees: PO, BA, backend lead, 2 frontend, 2 QA, Scrum Master. UX lead joined for the first 20 minutes.

## Decisions made
- Split EU2-S1. First version links to the upgrade journey and lets it fetch its own figure (no change to the journey). Refresh-on-expiry as a second story. Decided by: PO, with team agreement.
- Agreement Service can return a figure in real time; current 95th percentile is about 1.8 seconds. Backend lead.

## Actions
| Action | Owner | Due |
|---|---|---|
| Write story for audit logging of figures (Agreement Service doesn't log today) | PO | 20 Nov |
| Share draft card designs at 320px | UX lead | 22 Nov |
| Confirm support page URL | PO to chase Customer Ops lead | 22 Nov |

## Risks and issues raised
- Compliance copy not yet received; team can build with placeholder copy.
- Data engineering capacity for EU3-S2 is unconfirmed. **Unconfirmed**: Scrum Master to check.

## Proposed changes
See the "After the session" section of `08-refinement-pack.md`.

## Questions still open
- Validity period (Compliance).

## Rows to add to decisions.md
| 18 Nov | Split EU2-S1; MVP links to journey which fetches its own figure | Avoids change to upgrade journey team's code before spring | PO + team | Refinement 18 Nov |
