---
name: approve
description: "PO sign-off. Marks a draft artefact APPROVED, records who and when, and fingerprints the content."
argument-hint: <path to artefact> ["optional note"]
disable-model-invocation: true
---

The PO is signing off `$ARGUMENTS`.

1. Read the artefact. If it contains `[[OPEN]]` markers, list them and ask the PO to confirm they are happy to approve with those open. Stop if they say no.
2. Get the PO's name from `context/team-and-ways-of-working.md` ("Product Owner (signs off artefacts)").
3. Run: `python3 scripts/pdlc.py approve <path> --by "<PO name>" --note "<note, if given>"`
   Claude Code will ask the PO for permission. That prompt **is** the sign-off. Do not suggest "don't ask again".
4. If the script refuses because upstream isn't approved, tell the PO. Only add `--force` if they explicitly say so.
5. Confirm in one line, then show `python3 scripts/pdlc.py status <slug>` so they can see what's unlocked.
