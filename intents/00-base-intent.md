# Base Intent — Progressive AI Team

## Intent
Create a small AI-assisted team that completes one real recurring job for the user and proves measurable value before expanding.

## Inputs / Context
- The user does not want to manage implementation details or inspect code.
- Claude may choose the technical implementation.
- The experience should be simple and usable.
- The original giant-prompt concept is inspiration, not a specification.

## Outputs
- One working end-to-end job.
- A simple way for the user to trigger it.
- A concise result.
- Evidence that the result is correct/useful.
- A record of what should change next.

## Success Criteria
- The job works end-to-end.
- The user can understand what happened without reading code.
- Anything that sends, posts, pays, signs, deletes, or otherwise has external impact waits for explicit approval.
- Facts, numbers, links, and claims are checked or labeled uncertain.
- No duplicate agents or overlapping responsibilities.
- No infrastructure is added unless required by the job.

## Constraints
- One job first.
- One primary agent first.
- Prefer simple files/state before databases.
- Prefer local/manual execution before scheduled automation.
- Prefer deterministic checks for rules and approvals.
- Stop when success criteria are met.

## Evidence Required
- Example input.
- Example output.
- Validation result.
- Any failure encountered.
- Time or effort saved, if measurable.
