# Acceptance Checklist

Mark each item PASS / FAIL. Checked 2026-11-02.

- [x] **PASS** One real job was selected. — Personal productivity review.
- [x] **PASS** The workflow runs end-to-end. — `python3 run.py <notes>` → review → gate → saved run + log. 3/3 example runs.
- [x] **PASS** The user does not need to read code. — `RUNME.md` and `/review` in Claude Code.
- [x] **PASS** Output is understandable and useful. — Six plain sections with a one-line "why" per item.
- [x] **PASS** Factual claims are supported or qualified. — Every item cites its source line; gate fails on any mismatch; guessed ranks flagged under *Uncertain*.
- [x] **PASS** Consequential actions require approval. — Send/pay/sign/delete/etc. listed under *Needs Your Approval*, never executed; gate fails if one is missed or claimed as done.
- [x] **PASS** No duplicate agent roles exist. — One lead agent (`/review` command).
- [x] **PASS** No unnecessary infrastructure was added. — Python standard library, plain files. No DB, MCP, schedules, or dashboards.
- [x] **PASS** Feedback can be captured as KEEP / CHANGE / DROP. — Prompted at end of each run, or `--feedback`; logged.
- [x] **PASS** Evidence from the run is saved. — `runs/*/` (input, review, gate.json) and `evidence/runs.jsonl`.

Open: the `01-first-job` success criterion ("useful at least 2 of 3 times") needs **your** verdict on your own notes.
