# Instructions to Claude

Build this project from the intent files. Do not treat the folder as a request to create every possible component.

## Operating Rules

1. `intents/00-base-intent.md` is authoritative.
2. `intents/01-first-job.md` defines V1.
3. Do not implement future capabilities from `intents/02-progressive-intent.md` until evidence justifies them.
4. You own implementation choices. The user should not need to inspect code.
5. Prefer the simplest technology that can demonstrate the job.
6. Keep the UI simple and clear if a UI is needed.
7. Create tests or validation appropriate to the implementation.
8. Produce a short user-facing RUNME document with exact steps to use the result.
9. Produce an evidence report after the first successful run.

## Important

Do not generate a multi-agent architecture simply because the source image described one. Start with one lead agent. Promote repeated procedures into skills later. Use deterministic gates for approvals and quality checks.
