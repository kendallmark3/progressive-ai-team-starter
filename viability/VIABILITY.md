# Viability — Intent 01 (First Job)

**Verdict: VIABLE.** 4 of 5 held-out cases were useful with no intervention on the first try (bar: ≥2 of 3). After one evidence-driven fix, 5 of 5.

## Method
1. Wrote 5 new notes files the tool had never seen (`cases/`): architect workday, home errands, launch week, a deliberately vague list, and an incident firefight.
2. Wrote the expected answer for each **before running** (`expected.json`) and committed it (commit `c659604`). That way the bar couldn't move after the results came in.
3. Ran the job with no edits or retries (`python3 viability/score.py`). A case counts as **useful** only if all of these hold:
   - the quality gate didn't fail,
   - the top 3 holds at least 2 of the expected priorities,
   - every consequential item is flagged for approval,
   - every waiting and someday item lands in the right bucket,
   - the vague case admits its ranking is a guess.

## Run 1 — before any fix ([RESULTS.md](RESULTS.md))
| Case | Result | Note |
|---|---|---|
| 01 architect Monday | ❌ | Top 3 was perfect (3/3), but **"approve the vendor PO" wasn't flagged for approval** |
| 02 home errands | ✅ | Overdue registration and the leaking pump came first |
| 03 launch week | ✅ | 3/3 top; publish, delete and book were all flagged |
| 04 vague list | ✅ | Didn't invent urgency; said the ranking was a guess |
| 05 firefight | ✅ | 3/3 top; exec reply and AWS payment flagged; vendor block went to waiting |

**4/5 → VIABLE.**

## The failure, and the one change it justified
- **What happened:** approving a spend is consequential, but "approve" wasn't on the approval gate's word list.
- **Why it had to be fixed:** the base intent makes "wait for approval" non-negotiable. A miss here is a safety failure, not a matter of taste.
- **Change:** added `approve` and `authorize` to the list, plus a regression test. No new components.
- **Run 2** ([RESULTS-run2-after-fix.md](RESULTS-run2-after-fix.md)): 5/5.
- **Caveat:** run 2 reuses the same cases, so it shows the fix works. It isn't a fresh test of viability. Run 1 is the honest number.

## Weaknesses observed (not fixed — no evidence yet that they matter to you)
- **Weekday deadlines:** "party is saturday" isn't read as a deadline, so the birthday gift ranked below "groceries."
- **Urgency without keywords:** "it's leaking" doesn't count as urgent. The pump ranked #2 only because "call" counts as a quick win.
- **Quick-win bonus:** in the firefight, it pushed "reply to exec" (#1) above the live outage (#2). That's defensible, but it's a judgment call.

## What this does *not* prove
These are realistic notes I wrote, not your own notes. The intent's real bar is **you** running it 3 times on your own notes and saying KEEP at least twice. That verdict is the next piece of evidence needed.

## Next change
**NONE** until your feedback. If you answer CHANGE, the most likely first fix is reading weekday deadlines ("by Saturday", "on Friday").
