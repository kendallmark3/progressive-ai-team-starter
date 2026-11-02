# Shared Context

Keep shared state minimal and structured.

## User Goal
A small AI-assisted team that completes one real recurring job and proves value before expanding.

## Current Job
Personal productivity review — notes/tasks in, priorities and next actions out.

## Preferences
- Doesn't want to read code.
- Never perform consequential actions without approval.

## Approved Decisions
- V1 job: productivity review (built 2026-11-02).
- Implementation: Python standard library CLI + deterministic quality gate + `/review` Claude Code command.

## Open Questions
- Is the ranking useful on real notes?

## Last Result
3/3 example runs PASS WITH WARNINGS (all items verified; some ranks are guesses). One parse bug found and fixed.

## Feedback
_Pending_ — KEEP | CHANGE | DROP

## Next Evidence-Driven Change
NONE
