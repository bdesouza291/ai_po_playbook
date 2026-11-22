# Design notes

The decisions behind the kit, and what I traded off. Useful if you want to change it, and it's what I'd talk through if someone asked "why did you build it this way?"

## 1. Specialist agents, not one big prompt
Each stage has its own agent with its own instructions and a small set of tools. A discovery researcher needs to be sceptical about evidence; a story writer needs to know INVEST and Gherkin; a critic needs to be adversarial. Putting all of that in one prompt makes each part worse.

Subagents also run in their own context window, so the main conversation stays short and only gets the summary back. That matters on a Pro plan.

**Trade-off:** more files to maintain. Shared rules live in one block repeated in each agent, and in CLAUDE.md.

## 2. Gates between stages
Each stage reads only *approved* upstream artefacts. This stops a half-baked opportunity sizing from quietly becoming the PRD's success target. It also mirrors how good product teams work: you don't write stories against a PRD nobody has agreed.

**Trade-off:** it's slower than letting everything flow. `/override` exists for the times a real team would skip ahead, and it leaves a trace.

## 3. Sign-off enforced by tooling, not by asking nicely
Telling an AI "always ask before approving" works most of the time. "Most of the time" isn't good enough for an audit trail. So:
- the agents have no way to set the approved state (a hook blocks it),
- the only route is a script that Claude Code must ask permission to run,
- the content is fingerprinted, so later edits are visible.

**Trade-off:** depends on Python and on the user not running in bypass-permissions mode. `/setup-check` tests the hook.

## 4. Independent critic
The agent that wrote a draft is a poor judge of it. A separate critic with its own rubric, which hasn't seen the drafting conversation, finds different problems. It runs automatically for the three highest-stakes artefacts (PRD, backlog, release plan) and on request for the rest.

## 5. Evidence rules in every agent
Every number cites an input file or says Assumed. Quotes are copied, not invented. Findings are graded Strong / Moderate / Weak. This is the single biggest difference between useful and dangerous AI output in product work.

## 6. Recommend, don't decide
Prioritisation recommends, post-launch recommends, regulatory sections ask questions. Decisions are marked `[[OPEN]]` for the PO, and `/approve` warns if any are left. Real decisions go in `decisions.md` with who made them and why.

## 7. Plain markdown
Tool-neutral, diff-able in Git, pastes into Jira, Azure DevOps, Confluence or Notion. Front matter carries the status, version and sign-off fields.

**Next step if I were in a role:** connect the company's Jira and Confluence through MCP, and add a `/publish` command that pushes approved stories and pages. Approval would stay in this repo.

## 8. Writing style as a first-class input
Stakeholders stop reading the moment something sounds machine-written. `context/writing-style.md` bans the usual offenders and the critic checks for them.

## 9. Things I chose not to automate
- Estimation. The team estimates; agents may only flag "looks large".
- Applying meeting outcomes. The scribe proposes changes; the PO applies them.
- Anything that sends messages to people.

## Known weaknesses
- Agents can still misread evidence. The critic reduces this but doesn't remove it.
- The staleness check is time-based: it can't tell whether an upstream change actually affects the downstream artefact.
- The front-matter parser is deliberately simple (flat `key: value` only).
