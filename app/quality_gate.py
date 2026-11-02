"""Deterministic quality gate (hooks/quality-gate.md + hooks/approval-gate.md).

Checks a review against its source notes:
  1. Required sections exist.
  2. Every cited item (Ln) matches the source line verbatim  -> no fabrication.
  3. Every open source item appears exactly once in the ranked sections -> no drops/dupes.
  4. Every consequential item is listed under "Needs Your Approval".
  5. No claim that an external action was performed.
  6. Output is short enough to use.

Verdict: PASS | PASS WITH WARNINGS | FAIL

Usage:  python3 -m app.quality_gate <notes-file> <review-file>
"""
from __future__ import annotations

import json
import re
import sys

from app.review import parse, score, Item  # noqa: F401
from datetime import date

REQUIRED = ["## Top 3 Priorities", "## Next Actions", "## Waiting / Blocked",
            "## Defer or Drop", "## Needs Your Approval", "## Uncertain"]
RANKED = REQUIRED[:4]
CITE = re.compile(r"^(?:\d+\.|-)\s+(.*?)\s+—\s+.*\(L(\d+)\)\s*$")
DONE_CLAIMS = re.compile(r"\b(i|we|has been|have been|was|were|already)\s+(sent|posted|paid|signed|submitted|deleted|published|emailed|purchased)\b", re.I)
MAX_LINES = 80


def _sections(review: str) -> dict[str, list[str]]:
    cur, out = None, {}
    for line in review.splitlines():
        if line.startswith("## "):
            cur = line.strip(); out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def check(source: str, review: str) -> dict:
    errors, warnings = [], []
    src_lines = source.splitlines()
    secs = _sections(review)

    for s in REQUIRED:
        if s not in secs:
            errors.append(f"missing section: {s}")

    items, _ = parse(source)
    open_lines = {i.line: i for i in items}
    seen: dict[int, int] = {}

    for sec, lines in secs.items():
        for ln in lines:
            m = CITE.match(ln.strip())
            if not m:
                continue
            text, n = m.group(1).strip(), int(m.group(2))
            if n < 1 or n > len(src_lines) or text not in src_lines[n - 1]:
                errors.append(f"fabricated or mis-cited item: '{text}' (L{n})")
                continue
            if sec in RANKED:
                seen[n] = seen.get(n, 0) + 1

    for n, c in seen.items():
        if c > 1:
            errors.append(f"duplicate item L{n} appears {c} times")
    missing = [n for n in open_lines if n not in seen]
    for n in missing:
        errors.append(f"dropped item L{n}: '{open_lines[n].text}'")

    # approval gate: every consequential item must be surfaced for approval
    approval_cited = {int(m.group(2)) for ln in secs.get("## Needs Your Approval", [])
                      if (m := CITE.match(ln.strip()))}
    for it in items:
        score(it, date.today())
        if it.approval and it.line not in approval_cited:
            errors.append(f"consequential item L{it.line} not routed to approval: '{it.text}'")

    for ln in review.splitlines():
        if DONE_CLAIMS.search(ln) and not CITE.match(ln.strip()):
            errors.append(f"claims an external action was performed: '{ln.strip()}'")

    n_lines = len(review.splitlines())
    if n_lines > MAX_LINES:
        warnings.append(f"review is {n_lines} lines (> {MAX_LINES}); may be too long to use")
    unc = secs.get("## Uncertain", [])
    if any("guess" in l for l in unc):
        warnings.append("some rankings are guesses (no signal in source) — flagged to user")

    verdict = "FAIL" if errors else ("PASS WITH WARNINGS" if warnings else "PASS")
    return {"verdict": verdict, "errors": errors, "warnings": warnings,
            "items_checked": len(seen), "open_items": len(open_lines)}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__); return 2
    src = open(argv[1], encoding="utf-8").read()
    rev = open(argv[2], encoding="utf-8").read()
    res = check(src, rev)
    print(json.dumps(res, indent=2))
    return 1 if res["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
