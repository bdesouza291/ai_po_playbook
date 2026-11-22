# Setup guide

## What you need
- **Claude Code** (desktop app, CLI, or the VS Code extension). A Claude Pro plan works.
- **Python 3.8 or later.** Only the standard library is used, no installs.
- Optional: Git and a GitHub account if you want to publish it as a portfolio piece.

## 1. Check Python
Open a terminal:
- Mac / Linux: `python3 --version`
- Windows: `python --version` (and `python3 --version`; on some Windows machines `python3` opens the Microsoft Store instead)

If neither works, install Python from python.org. On Windows, tick **"Add python.exe to PATH"** in the installer.

## 2. Open the project in Claude Code
Unzip the folder somewhere sensible, for example `Documents/po-agent-kit`.
- **Desktop app:** start a new Code session and choose this folder.
- **CLI:** `cd` into the folder and run `claude`.

The first time, Claude Code asks whether you trust the folder. Say yes, otherwise the project's permission rules and hook won't load.

## 3. Run the setup check
Type `/setup-check`. It checks Python, the ledger script, and that the sign-off guard blocks what it should. You should see two "blocked" results; that's the guard working.

**If the guard tests aren't blocked** (most likely on Windows):
1. Check which Python command works (step 1).
2. Open `.claude/settings.json`. The hook command is a small shell snippet that tries `python3` and falls back to `python`. Replace the whole `"command"` value with a direct call, for example:
   `"command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py\""`
   or, if `python` isn't on PATH, the full path to it, such as `C:/Users/you/AppData/Local/Programs/Python/Python312/python.exe`.
3. Run `/setup-check` again. If it still isn't blocked, ask Claude in the session to debug the hook; it can read the hook output.

## 4. Make it yours
Edit these before your first real initiative:
- `context/product-context.md`: product, customers, strategy, systems
- `context/team-and-ways-of-working.md`: your name as the signing PO, team, DoR, DoD
- `context/regulatory-notes.md`: replace with your employer's guidance when you have it

## 5. Your first initiative
```
/new-initiative early-upgrade "Let mid-contract customers upgrade online"
```
Answer the brief questions. Then:
1. Add evidence to `work/early-upgrade/inputs/` (notes, CSVs, exports, screenshots described in text).
2. `/approve work/early-upgrade/00-brief.md` and allow the permission prompt.
3. `/discover early-upgrade`
4. Read the draft. Give feedback with `/discover early-upgrade <your feedback>` or approve it.
5. `/next early-upgrade` whenever you're not sure what's next.

## Tips for a Pro plan
- Do one or two stages per session. Start a fresh session for the next stage; everything the agents need is in the files.
- Keep `inputs/` focused. Ten relevant files beat fifty.
- If you hit a usage limit mid-stage, the draft is already on disk. Pick up where you left off.

## Approval prompts
When `/approve` runs, Claude Code shows a permission prompt for `pdlc.py approve`. That's your signature. **Don't choose "don't ask again"**: the project rules keep asking anyway, but it's a good habit. Don't run the kit in bypass-permissions mode.

## Publishing to GitHub (portfolio)
1. Read through `examples/` and the context files and make sure you're happy with everything in them. All example data is fictional.
2. In the folder: `git init`, `git add .`, `git commit -m "PO Agent Kit"`.
3. Create an empty repository on GitHub, then follow its "push an existing repository" instructions. GitHub Desktop works too.
4. Pin the repository on your GitHub profile. The README renders the flow diagram.

Keep real work out of a public repo. When you use this in a job, keep `work/` in your employer's systems, not on GitHub. `.gitignore` already excludes `work/*` except the placeholder.
