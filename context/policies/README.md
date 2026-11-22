# Policies

Drop your organisation's real policy and standards documents here — the ones a Product Owner must honour when specifying work. This folder is the kit's generalised version of a company "policy library": a place agents can read from when a change touches a governed area.

## How to use it
- Put one policy per file, in Markdown where you can (agents read Markdown best). PDFs and `.docx` work too but agents can only skim them.
- Group them in subfolders if you have a lot — e.g. `security/`, `data-protection/`, `accessibility/`, or by product line.
- Keep the filename meaningful and versioned, e.g. `data-retention-v4-2026.md`.

## How agents use it
- When a PRD or story touches a governed area, agents raise it under **"Regulatory and compliance considerations"** as a **question for Compliance**, and cite the specific policy file here rather than paraphrasing law.
- Agents never declare something "compliant". They point at the policy and name who should confirm.
- Keep `context/regulatory-notes.md` as the short index of *which* areas matter; keep the full text here.

## What not to put here
- Secrets, credentials, or personal data. This is a policy library, not a data store.
- One-off evidence for a specific initiative — that goes in `work/<slug>/inputs/`.

See `_example-policy.md` for the shape of a good entry.
