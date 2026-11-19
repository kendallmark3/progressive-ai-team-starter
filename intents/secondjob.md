Intent Refiner — Give it a rough story or idea and have it produce a clean intent with Intent / Inputs / Outputs / Success Criteria, while flagging anything that is over-specified. This is probably the most directly useful one for you.

Progressive Intent Runner — Feed it the current intent + evidence/tests/results. It decides: Are we done? If not, what is the minimum next intent? No giant upfront plan. This directly exercises your “don’t spend any token before its time” idea.

Architecture Radius Reviewer — Point it at a repo or proposed system and have it examine R1–R5: local code → application → platform/network → enterprise controls → external systems/providers. Output gaps, evidence, risks, and what actually needs attention.

Intent Drift Detector — Compare the original human intent to what the agents actually built. It should say things like: met / partially met / drifted / added unnecessary scope / success criteria unsupported by evidence. This one could become extremely valuable on larger AI teams.

Deterministic-vs-Agentic Advisor — Give it a proposed feature or workflow and make it classify each part: Human declares → Agent reasons → System verifies. Then recommend what belongs in a Skill, Hook, MCP/tool, subagent, ordinary code, or nowhere at all.