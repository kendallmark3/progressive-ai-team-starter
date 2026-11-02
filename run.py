#!/usr/bin/env python3
"""Run the V1 job: productivity review -> quality gate -> evidence.

    python3 run.py my-notes.md
    python3 run.py my-notes.md --feedback KEEP
    cat notes.txt | python3 run.py -
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.review import review  # noqa: E402
from app.quality_gate import check  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Productivity review with a quality gate.")
    ap.add_argument("notes", help="notes/tasks file, or - for stdin")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--feedback", choices=["KEEP", "CHANGE", "DROP"], type=str.upper)
    ap.add_argument("--note", default="", help="optional feedback comment")
    a = ap.parse_args()

    raw = sys.stdin.read() if a.notes == "-" else Path(a.notes).read_text(encoding="utf-8")
    today = date.fromisoformat(a.today) if a.today else date.today()
    name = "stdin" if a.notes == "-" else Path(a.notes).name

    started = datetime.now()
    text = review(raw, today=today, source=name)
    gate = check(raw, text)
    elapsed = (datetime.now() - started).total_seconds()

    stamp = started.strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{stamp}-{Path(name).stem}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "input.md").write_text(raw, encoding="utf-8")
    (run_dir / "review.md").write_text(text, encoding="utf-8")
    (run_dir / "gate.json").write_text(json.dumps(gate, indent=2), encoding="utf-8")

    print(text)
    print(f"Quality gate: {gate['verdict']}  ({gate['items_checked']}/{gate['open_items']} items verified against source)")
    for e in gate["errors"]:
        print(f"  ERROR: {e}")
    for w in gate["warnings"]:
        print(f"  warning: {w}")

    fb = a.feedback
    if not fb and sys.stdin.isatty() and a.notes != "-":
        ans = input("\nKEEP / CHANGE / DROP (Enter to skip)? ").strip().upper()
        fb = ans if ans in ("KEEP", "CHANGE", "DROP") else None

    record = {"time": started.isoformat(timespec="seconds"), "input": name, "run_dir": str(run_dir.relative_to(ROOT)),
              "verdict": gate["verdict"], "errors": len(gate["errors"]), "warnings": gate["warnings"],
              "items": gate["open_items"], "seconds": round(elapsed, 3), "feedback": fb, "note": a.note}
    log = ROOT / "evidence" / "runs.jsonl"
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print(f"\nSaved: {run_dir.relative_to(ROOT)}/  ·  logged to evidence/runs.jsonl")
    return 1 if gate["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
