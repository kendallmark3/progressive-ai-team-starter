# Intent 01 — Choose and Build the First Job

## Intent
Choose one useful recurring job and build the smallest version that can complete it reliably.

## Candidate Jobs
Choose only one:

1. Research brief — user gives a topic; system gathers, checks, and summarizes useful information.
2. Inbox triage — system summarizes messages and drafts recommended responses, but does not send.
3. Calendar preparation — system prepares a meeting brief and action list, but does not modify the calendar without approval.
4. Content assistant — system turns a rough idea into a draft, with evidence for factual claims.
5. Personal productivity review — system takes notes/tasks and returns priorities and next actions.

## Selection Rule
Prefer the job that:
- happens repeatedly,
- can save meaningful time,
- has clear inputs and outputs,
- can be tested immediately,
- and has low consequence if imperfect.

## V1 Scope
- One user input.
- One primary worker.
- One output.
- One quality check.
- One short feedback question: KEEP / CHANGE / DROP.

## Do Not Add Yet
- multi-agent orchestration,
- background schedules,
- external writes,
- complex memory,
- dashboards,
- MCP servers,
- databases,
- autonomous action loops.

## Success Criteria
The user can run the chosen job three times and gets useful results at least two times without intervention.
