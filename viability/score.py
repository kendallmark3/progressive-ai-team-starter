#!/usr/bin/env python3
"""Score the V1 job against pre-registered expected answers.

    python3 viability/score.py
Runs run.py on every case (no intervention), then grades each against expected.json.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "viability"
exp = json.loads((V / "expected.json").read_text())


def section(review: str, name: str) -> str:
    return review.split(f"## {name}")[1].split("\n## ")[0] if f"## {name}" in review else ""


results, out = [], ["# Viability Results", "", f"Today fixed at {exp['today']}. Expected answers committed before any run.", ""]
for case, e in exp["cases"].items():
    p = subprocess.run([sys.executable, "run.py", str(V / "cases" / case), "--today", exp["today"]],
                       cwd=ROOT, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    review = p.stdout.split("Quality gate:")[0]
    gate = p.stdout.split("Quality gate:")[1].split()[0] if "Quality gate:" in p.stdout else "?"
    gate_fail = "FAIL" in p.stdout.split("Quality gate:")[1].split("(")[0] and "WARN" not in p.stdout.split("Quality gate:")[1].split("(")[0]
    top = section(review, "Top 3 Priorities")
    checks = []
    checks.append(("gate not FAIL", not gate_fail))
    if e["expected_top"]:
        hit = [t for t in e["expected_top"] if t in top]
        checks.append((f"top-3 has >=2 expected ({len(hit)}/3: {', '.join(hit) or '-'})", len(hit) >= 2))
    for t in e["expected_approval"]:
        checks.append((f"approval flagged: {t}", t in section(review, "Needs Your Approval")))
    for t in e["expected_waiting"]:
        checks.append((f"waiting: {t}", t in section(review, "Waiting / Blocked")))
    for t in e["expected_defer"]:
        checks.append((f"deferred: {t}", t in section(review, "Defer or Drop")))
    if e.get("expect_uncertain_flag"):
        checks.append(("honestly flags ranking as a guess", "guess" in section(review, "Uncertain")))
    useful = all(ok for _, ok in checks)
    results.append(useful)
    out += [f"## {case} — {'USEFUL' if useful else 'NOT USEFUL'}  (gate: {p.stdout.split('Quality gate: ')[1].split('  (')[0]})", ""]
    out += [f"- {'✅' if ok else '❌'} {c}" for c, ok in checks]
    out += ["", "<details><summary>Top 3 produced</summary>", "", top.strip(), "", "</details>", ""]

n, k = len(results), sum(results)
verdict = "VIABLE" if k / n >= 2 / 3 else "NOT VIABLE"
out.insert(3, f"**{k}/{n} useful without intervention → {verdict}** (bar: ≥2 of 3)\n")
(V / "RESULTS.md").write_text("\n".join(out))
print("\n".join(out))
sys.exit(0 if verdict == "VIABLE" else 1)
