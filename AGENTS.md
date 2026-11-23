# Repository instructions

This repository is an agent-driven Product Owner template. Keep it reusable, evidence-led and tool-neutral.

## Source of truth

- `CLAUDE.md` defines the Claude-specific PDLC orchestration and sign-off protocol.
- `context/` defines product, team and writing context. Never infer facts that the context or evidence does not support.
- `templates/` defines stage artefact structure.
- `scripts/pdlc.py` owns the sign-off ledger, gates, fingerprints and staleness checks.
- `.claude/hooks/guard.py` is the local safety boundary for approved artefacts.

## Change rules

- Preserve the human Product Owner approval boundary. Agents draft; they do not approve, reopen or override.
- Do not put secrets, credentials or real customer data in `examples/`, `context/`, commits or logs.
- Keep stable requirement, story and test scenario IDs unchanged once they are referenced downstream.
- Keep `full` and `lite` track behavior working together.
- Use plain, evidence-led Markdown. Cite an input or upstream artefact, or label a claim `Assumed`.
- Do not estimate team effort or state that a change is compliant.
- Update directly related documentation and tests with behavior changes.

## Validation

Before a commit, run:

```powershell
python scripts/validate_template.py
python scripts/test_pdlc.py
python scripts/test_guard.py
python scripts/pdlc.py context-check
python scripts/pdlc.py trace flexpay-early-upgrade
```

On Linux or macOS, use `python3` if that is the available interpreter.

## Cross-agent setup

Reusable skills mirror the Claude definitions under `.agents/skills/`. Prefer the mirror for Codex, Cursor and other agents that read `.agents/skills/`. After changing `.claude/skills/`, mirror it and run `validate_template.py`.
