# Progressive Intent — What to Add Next

Use this file only after V1 has been run and evidence exists.

## Rule
Add the minimum next constraint or capability required by observed evidence.

## Evidence-Driven Triggers

### Add a Skill when
The same successful procedure is repeated at least twice and should become reusable.

### Add a Specialized Agent when
A distinct reasoning role repeatedly degrades quality when handled by the primary worker, or can be parallelized independently.

### Add a Hook when
A rule must be enforced deterministically every time, such as approval, schema validation, evidence presence, or prohibited actions.

### Add Shared Context when
The system repeatedly loses important state between steps.

### Add Automation when
The manual workflow is stable and the user explicitly benefits from recurring execution.

### Add an Integration / MCP Connector when
A real source or action is repeatedly needed and manual access is the bottleneck.

## Overwritten-Intent Check
Before adding anything, ask:
- Does this change preserve the original outcome?
- Is it solving an observed problem or an imagined future problem?
- Could a simpler constraint solve it?

## Stop Condition
If the current system meets success criteria, stop building.
