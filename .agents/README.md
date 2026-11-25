# Cross-agent skills

This directory mirrors `.claude/skills/` for coding agents that load skills from `.agents/skills/`.

- The Claude folder is the source of truth.
- The mirror is generated and byte-for-byte identical. Never edit it by hand.
- Agent-specific slash-command syntax may differ; the workflow and approval rules do not.
- Agents still must not approve, reopen or override artefacts unless the human explicitly invokes that action.

After changing a skill, run `python scripts/sync_mirror.py`, then `python scripts/validate_template.py`. `sync_mirror.py --check` fails if the mirror is stale.
