# Regulatory and compliance prompts

> Prompts for the PO to raise with Compliance / Legal. **Not legal advice**, and may be out of date. Replace the rows below with your own sector's obligations, or point agents at `context/policies/` for your organisation's actual policy documents.
> A worked example for UK handset financing lives in `examples/flexpay-early-upgrade/context-snapshot/regulatory-notes.md`.

Use this file to list the areas an agent should surface as **questions for Compliance** whenever a change touches them.

| Area | What to ask about | Typical product impact |
|---|---|---|
| <regime / duty> | <the question the PO should put to Compliance> | <what it tends to change in the product> |
| Data protection (e.g. UK GDPR) | What personal data do we use, why, and for how long? | Data minimisation, privacy notice, retention |
| Accessibility | What is our required bar (e.g. WCAG 2.2 AA)? | Design and test effort |
| Record-keeping / audit | What must be stored, and for how long, to evidence the decision? | Audit trail, document generation |
| Complaints / customer harm | How are issues with this journey logged and routed? | Contact reasons, tagging, escalation routes |

## How agents should use this file
- Raise relevant rows under "Regulatory and compliance considerations" as **questions for Compliance**, not as statements of law.
- Never tell the PO that something is compliant. Say what needs checking and who should check it.
- Where your organisation has written policies, keep them in `context/policies/` and cite the specific policy rather than paraphrasing it.
