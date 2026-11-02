# RUNME — Productivity Review (V1)

**What it does:** you paste your messy notes or task list; it hands back your top 3 priorities, next actions, what's waiting on others, what to defer, and anything that needs *your* approval (sending, paying, signing, deleting). It never does those things itself.

Every line in the result points back to the line in your notes it came from (`L4` = line 4), and a quality gate checks that nothing was invented, dropped, or duplicated.

## Needs
Python 3.9+. Nothing to install.

## Use it

1. Put your notes in a file — any format: bullets, `- [ ]` checkboxes, numbered, or plain lines.
   Add a date like `2026-11-05` or words like `urgent`, `tomorrow`, `client` to sharpen ranking.
2. Run:
   ```bash
   python3 run.py my-notes.md
   ```
3. Read the review. At the end it asks **KEEP / CHANGE / DROP** — type one and press Enter.

That's it. The result is also saved in `runs/<timestamp>-<name>/` and the run is logged to `evidence/runs.jsonl`.

### Other ways
```bash
pbpaste | python3 run.py -                       # straight from your clipboard (macOS)
python3 run.py my-notes.md --feedback CHANGE --note "rank client work higher"
```

### From Claude Code
Open this folder in Claude Code and type:
```
/review my-notes.md
```
Claude runs the review, checks the gate, and adds a short plain-English take — without adding anything that isn't in your notes.

## Try it now
```bash
python3 run.py examples/monday-work.md
```

## Reading the result
| Section | Meaning |
|---|---|
| Top 3 Priorities | Do these first. The italic note says why. |
| Next Actions | Everything else that's open, in priority order. |
| Waiting / Blocked | Ball's in someone else's court. |
| Defer or Drop | Marked someday/maybe/nice-to-have. |
| Needs Your Approval | Has an external consequence. Not done — yours to do. |
| Uncertain | Where the ranking is a guess. |

**Quality gate:** `PASS` = verified. `PASS WITH WARNINGS` = verified, but some ranks are guesses. `FAIL` = don't trust it; the errors say why.

## Check it works
```bash
python3 -m unittest discover -s tests
```
