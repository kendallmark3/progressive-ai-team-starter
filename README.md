# Progressive AI Team Starter

> **V1 is built.** Job: *personal productivity review*. Start with [`RUNME.md`](RUNME.md) — `python3 run.py examples/monday-work.md`.
> Evidence: [`evidence/run-report.md`](evidence/run-report.md) · Checklist: [`evidence/acceptance-checklist.md`](evidence/acceptance-checklist.md)

This starter turns the giant “AI team” prompt into a progressive, intent-driven structure. The goal is to let Claude build the implementation without requiring you to inspect code.

## Principle

Start with one real job. Add only the minimum structure needed to make that job work. Promote repeated behavior into reusable skills only after it proves useful.

> Don't spend any token before its time.

## What Claude should build first

1. Read `intents/00-base-intent.md`.
2. Ask at most five questions only if the missing information blocks implementation.
3. Select one useful first job from `intents/01-first-job.md`.
4. Implement the smallest working version.
5. Run the validation in `evidence/acceptance-checklist.md`.
6. Record evidence in `evidence/run-report.md`.
7. Read `intents/02-progressive-intent.md` before adding anything else.

Do **not** build multiple agents, complex memory, automation, MCP integrations, or dashboards unless the evidence shows they are needed.

## Structure

- `intents/` — human-owned outcomes, boundaries, success criteria, and progressive deltas
- `skills/` — reusable capabilities that emerge after repetition
- `agents/` — specialized reasoning roles only when one role cannot do the job well
- `hooks/` — deterministic enforcement and approval gates
- `context/` — shared structured state and handoff format
- `workflows/` — workflow maps, not implementation details
- `evidence/` — acceptance criteria and proof of what actually worked
- `docs/` — architecture notes and Claude build instructions

## Definition of success

The first version succeeds when one real job can be completed end-to-end with:

- a clear user request,
- a useful result,
- visible evidence,
- no fabricated facts,
- approval before consequential actions,
- and no unnecessary infrastructure.

After that, improve only from observed failures or repeated work.
