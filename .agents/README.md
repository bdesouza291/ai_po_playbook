# Cross-agent skills

This directory mirrors `.claude/skills/` for coding agents that load skills from `.agents/skills/`.

- The Claude folder is the source of truth.
- Keep mirrored `SKILL.md` files byte-for-byte identical.
- Agent-specific slash-command syntax may differ; the workflow and approval rules do not.
- Agents still must not approve, reopen or override artefacts unless the human explicitly invokes that action.

Run `python scripts/validate_template.py` after changing a skill.
