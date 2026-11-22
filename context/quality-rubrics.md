# Quality rubrics

The `artefact-critic` agent scores drafts against these. Each check is Pass / Weak / Fail with a one-line reason and a suggested fix.

## Applies to every artefact
1. **Traceable:** every claim, number and quote points to an input file or an upstream artefact, or is labelled Assumed.
2. **Honest about gaps:** assumptions and open questions are listed, not hidden in prose.
3. **Scoped:** says what it does not cover.
4. **Readable:** follows `writing-style.md`. A stakeholder could read the summary in under a minute.
5. **Consistent:** no contradictions with approved upstream artefacts (names, numbers, scope).
6. **No overreach:** recommends, does not decide. Never claims something is compliant.

## Discovery
- Findings separate observation from interpretation.
- Evidence strength is graded, and Weak findings aren't presented as facts.
- Missing voices (segments not in the evidence) are named.

## Opportunity
- Problem statement names a segment, a cause and an impact.
- Sizing shows arithmetic with low / likely / high, and each input is Known or Assumed.
- Riskiest assumption has a concrete, cheap test.

## Prioritisation
- At least three genuinely different options, including "do nothing / minimal".
- Scores show inputs. Effort is marked as a placeholder until the team estimates.
- Recommendation states what we give up and what would change the call.

## PRD
- Goals have baselines and targets; non-goals exist.
- Requirements have stable IDs (`<AREA>.<GROUP>.<ITEM>`) and each has at least one BDD acceptance scenario with its own scenario ID.
- NFRs cover accessibility, performance, privacy and audit.
- Regulatory section raises questions, not conclusions.
- Doesn't design APIs or architecture for the team.

## Metrics plan
- Primary, secondary and guardrail metrics defined with numerator / denominator.
- Experiment has a sample size calculation or an explicit reason why not.
- Every event in the tracking plan maps to a story.

## Backlog
- Stories are vertical, INVEST, and fit in a sprint.
- Each story has at least one negative-path scenario.
- Every PRD Must-have maps to at least one story (traceability table complete).
- Analytics stories exist for the tracking plan.

## Test scenarios
- Covers happy, negative, edge, accessibility and analytics.
- Lists test data needs.
- Flags AC gaps back to the backlog.

## Refinement pack
- Questions are specific enough to answer in the room.
- Large stories have at least two split options.

## Release plan
- Rollout phases have entry and exit criteria.
- Rollback triggers are measurable.
- Support readiness and comms sign-off are on the checklist.

## Comms
- Each audience gets what it cares about, at the right length.
- Customer copy is plain, flags anything needing compliance review.

## Post-launch review
- Results compared to targets with confidence noted.
- Recommendation is clear, follow-ups are backlog-ready.

## Build spec (handoff)
- **Self-contained:** a developer or AI coding agent could build it without opening another document.
- Story, requirement blocks and acceptance scenarios match the backlog and PRD **word for word**, with every scenario ID tag present (check against `pdlc.py story`).
- Out of scope is explicit, including what sibling stories cover, so the builder doesn't drift into them.
- Every scenario has test intent: a level, an owner, and the rule to tag the test with the scenario ID.
- Builder context is honest: real pointers where known, `[[TECH LEAD]]` where not. No invented repo paths, APIs or table names.
- Open questions are either empty or explicitly accepted for build, each with an owner.
- The "Rules for AI coding agents" block is present and unchanged.

## Close report
- Delivery status per requirement comes from `pdlc.py trace --evidence`, not from reading the files.
- Every Must requirement that isn't Implemented (full) has a reason and a follow-up: a story, a defect, or a recorded descope decision.
- Follow-up stories reference the original requirement and scenario IDs; no ID is reused or renumbered.
- Spec drift (what shipped differs from the PRD) is raised as a proposed `/reopen`, not edited silently.
- The verdict is one of: Close / Close with follow-ups / Not ready to close, with the reason.
