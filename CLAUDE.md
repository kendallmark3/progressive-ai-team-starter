# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An intent-driven starter whose one built job (V1) is a **personal productivity review**: notes in; priorities, next actions, and approval flags out. It is a deterministic CLI with no LLM calls. It needs Python 3.9+ and only the standard library.

The owner does not want to read code. Report results in plain English, and keep `RUNME.md` accurate for someone who won't open the source.

## Commands

```bash
python3 run.py examples/monday-work.md          # run the job (also: `-` for stdin, --today YYYY-MM-DD)
python3 run.py notes.md --feedback CHANGE --note "why"   # log KEEP/CHANGE/DROP without the prompt
python3 -m app.quality_gate <notes> <review>    # run the gate alone on an existing review
python3 -m unittest discover -s tests           # all tests
python3 -m unittest tests.test_v1.ReviewTests.test_deterministic   # one test
python3 viability/score.py                      # grade the held-out cases
```

There is no build step or linter. `/review <notes-file>` ([.claude/commands/review.md](.claude/commands/review.md)) wraps `run.py` for use inside Claude Code.

**Commands that change tracked files:**
- `run.py` creates a `runs/<timestamp>-<name>/` directory and appends to `evidence/runs.jsonl`. Both are committed as evidence, so a run dirties the tree.
- `viability/score.py` calls `run.py` for each case and **overwrites `viability/RESULTS.md`**, which is the record of run 1, the number cited as the honest viability result. If you re-score, restore that file or move the new output to a separate file, as was done for `RESULTS-run2-after-fix.md`.

## Architecture

The pipeline is `run.py` → `app/review.py` (`review`) → `app/quality_gate.py` (`check`) → evidence on disk. `run.py` exits 1 when the gate verdict is `FAIL`.

The gate works by re-parsing the source notes and comparing them with the rendered Markdown, which couples the two modules in ways that aren't visible from either file alone:

- **The output format is the gate's contract.** Each item row must match the `CITE` regex (`text — why (Ln)`), and the section headings must match `REQUIRED`. Changing how `review()` renders means changing the gate too.
- **Each open item must appear exactly once across the four ranked sections** (Top 3, Next Actions, Waiting, Defer). "Needs Your Approval" is separate, so an item appears there *in addition to* its ranked section.
- **The gate shares `parse` and `score` with the reviewer**, including the `CONSEQUENTIAL` word list. A word missing from that list gets past both, so the gate can't catch it. That is how "approve the vendor PO" passed the gate in viability run 1.
- **Prose-to-code mapping:** the `hooks/*.md` files are written specs, not Claude Code hooks. Their rules are enforced by `quality_gate.py`. Likewise, `agents/` and `skills/` are not registered with Claude Code; only `.claude/commands/review.md` is live.

Ranking is keyword scoring over the vocabulary lists at the top of `review.py`. Output must stay deterministic for the same input and date, so pass `--today` or a fixed date when comparing runs.

## Rules for changing this repo

`intents/00-base-intent.md` is authoritative, and `intents/01-first-job.md` defines V1 scope.

- **Change only on evidence.** Read `intents/02-progressive-intent.md` before adding anything; each capability has a trigger there. Don't add agents, skills, schedules, integrations, MCP servers, databases, or dashboards without observed evidence that the job needs them. If success criteria are met, stop.
- **Next change is currently NONE.** It is waiting on the owner's KEEP/CHANGE/DROP verdict on their own notes (`viability/VIABILITY.md`, `context/shared-context.md`). Known weaknesses listed in `VIABILITY.md`, such as weekday deadlines, are deliberately unfixed.
- **Never perform consequential actions.** The tool only flags sending, paying, signing, deleting, and similar actions (`hooks/approval-gate.md`). The review must not claim one was done, and it must not invent tasks, dates, people, or facts.
- **Keep viability testing honest.** Commit expected answers in `viability/expected.json` before running new cases, and don't edit them afterward to fit results. A re-run on the same cases shows a fix works, not that the tool is viable.
- **Fix failures with a regression test**, as `test_approving_spend_is_consequential` does, and record what happened in `evidence/` or `viability/`.
