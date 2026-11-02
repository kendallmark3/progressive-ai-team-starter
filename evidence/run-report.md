# Run Report

## Date
2026-11-02

## Job
**Personal productivity review** (candidate 5 in `intents/01-first-job.md`).
Chosen because it recurs daily/weekly, has clear text-in/text-out, can be tested immediately, and is low-consequence if imperfect. It needs no external sources, so there are no facts to fabricate — every output line is traceable to an input line.

## User Input
Three sample inputs in `examples/` (work brain-dump with checkboxes, plain-line home list, messy standup notes in mixed formats). Full inputs and outputs saved in `runs/`.

## Result
Example (`examples/monday-work.md`, today = 2026-11-02):

```
## Top 3 Priorities
1. Finish Q4 architecture deck for VP review 2026-11-03 — due 2026-11-03; high-stakes: vp (L3)
2. Prep demo for client kickoff tomorrow — soon: tomorrow; high-stakes: client, demo (L10)
3. Reply to Priya about the interview loop — high-stakes: interview; quick win (L4)
## Needs Your Approval
- Reply to Priya about the interview loop — action: reply (L4)
- Submit expense report by Friday — action: submit (L8)
```

## Validation
**PASS WITH WARNINGS** — 3 of 3 runs.

| Run | Open items | Verified vs source | Errors | Warning |
|---|---|---|---|---|
| home-week.md | 7 | 7/7 | 0 | some ranks are guesses (no signal) |
| messy-notes.txt | 6 | 6/6 | 0 | some ranks are guesses (no signal) |
| monday-work.md | 8 | 8/8 | 0 | some ranks are guesses (no signal) |

13 unit tests pass, including 5 that prove the gate FAILs on fabricated items, dropped items, duplicates, consequential items not routed to approval, and claims that an action was performed.

## What Worked
- Dated, overdue, and urgent items consistently land in Top 3.
- Waiting/blocked and someday items are separated out.
- Every pay/sign/delete/cancel/order/submit/reply item is surfaced for approval; nothing is executed.
- Mixed formats (checkbox, numbered, `*`, `+`, plain lines) parse correctly; completed `[x]` items and quotes are skipped.

## What Failed
- **First run of `messy-notes.txt`:** the label line `notes from standup:` was ranked as a task (#3 priority). Fixed: lines ending in `:` that aren't bullets are treated as context. Regression test added. Re-run passes.
- **Known limit (not fixed):** items with no date or keyword are ranked by original order. The review says so under *Uncertain* rather than pretending to know.

## User Feedback
_Pending — awaiting your KEEP / CHANGE / DROP on a run with your own notes._

## Time / Effort Saved
Not yet measurable — needs real runs on your notes. Runtime is ~5 ms per review.

## Next Change
**NONE** until real-use feedback exists. Most likely candidate if you answer CHANGE: let you set your own priority keywords (e.g. a project name) in a small text file — a constraint, not new infrastructure.
