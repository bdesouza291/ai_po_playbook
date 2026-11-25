---
name: approve
description: "PO sign-off. Marks a draft artefact APPROVED, records who and when, and fingerprints the content."
argument-hint: <path to artefact> ["optional note"]
disable-model-invocation: true
---

The PO is signing off `$ARGUMENTS`.

1. Read the artefact. If it contains `[[OPEN]]` markers, list them and ask the PO to confirm they are happy to approve with those open. Stop if they say no.
2. Run: `scripts/pdlc approve <path> --note "<note, if given>"`. Do not pass `--by`: the script reads the signer from the PO named in `context/team-and-ways-of-working.md`, and stops with a message if that file has no name (suggest `/onboard`).
   Claude Code will ask the PO for permission. That prompt **is** the sign-off. Do not suggest "don't ask again".
3. If the script refuses because upstream isn't approved, tell the PO. Only add `--force` if they explicitly say so, and it needs their reason: `--force --reason "<their words>"`. Ask for it; never write one yourself.
4. Confirm in one line, then show `scripts/pdlc status <slug>` so they can see what's unlocked.
