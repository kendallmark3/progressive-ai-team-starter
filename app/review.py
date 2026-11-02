"""V1 job: Personal productivity review.

Takes a plain notes/tasks file and returns priorities and next actions.
Every item in the output cites the input line it came from (Ln), so the
quality gate can prove nothing was invented, dropped, or duplicated.

Standard library only. Deterministic: same input + same date = same output.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta

# --- signal vocab -----------------------------------------------------------

URGENT = ["today", "asap", "urgent", "eod", "tonight", "now", "overdue", "immediately"]
SOON = ["tomorrow", "this week", "by monday", "by tuesday", "by wednesday",
        "by thursday", "by friday", "this weekend", "deadline", "due"]
IMPORTANT = ["boss", "client", "customer", "exec", "ceo", "vp", "critical", "launch",
             "demo", "production", "prod", "outage", "blocker", "security", "audit",
             "contract", "renewal", "interview"]
QUICK = ["quick", "5 min", "10 min", "reply", "call", "text", "confirm", "rsvp"]
WAITING = ["waiting on", "waiting for", "blocked by", "blocked on", "pending", "awaiting"]
DEFER = ["someday", "maybe", "idea:", "nice to have", "eventually", "later", "if time"]
# Consequential actions: the system never performs these. It flags them as yours.
CONSEQUENTIAL = ["send", "email", "post", "publish", "pay", "purchase", "buy", "sign",
                 "submit", "delete", "remove", "cancel", "wire", "transfer", "order",
                 "book", "reply", "approve", "authorize"]

BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])?\s*(?:\[( |x|X)\])?\s*")
ISO_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def _has(text: str, words: list[str]) -> list[str]:
    low = text.lower()
    hits = []
    for w in words:
        pattern = r"(?<![a-z])" + re.escape(w) + r"(?![a-z])"
        if re.search(pattern, low):
            hits.append(w)
    return hits


@dataclass
class Item:
    line: int
    text: str
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    bucket: str = "next"          # next | waiting | defer
    approval: list[str] = field(default_factory=list)
    quick: bool = False


def parse(raw: str) -> tuple[list[Item], int]:
    """Return active items and the count of skipped completed items."""
    items, done = [], 0
    for n, line in enumerate(raw.splitlines(), start=1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">"):
            continue
        if s.endswith(":") and not BULLET.match(line).group(0).strip():
            continue  # a label like "notes from standup:" is context, not a task
        m = BULLET.match(line)
        if m and m.group(1) in ("x", "X"):
            done += 1
            continue
        text = line[m.end():].strip() if m else s
        if text:
            items.append(Item(line=n, text=text))
    return items, done


def score(item: Item, today: date) -> Item:
    t = item.text
    if hits := _has(t, WAITING):
        item.bucket = "waiting"
        item.reasons.append(f"waiting ({hits[0]})")
    elif hits := _has(t, DEFER):
        item.bucket = "defer"
        item.reasons.append(f"deferrable ({hits[0]})")

    for d in ISO_DATE.findall(t):
        try:
            due = date.fromisoformat(d)
        except ValueError:
            item.reasons.append(f"unreadable date {d}")
            continue
        delta = (due - today).days
        if delta < 0:
            item.score += 5; item.reasons.append(f"overdue since {d}")
        elif delta <= 1:
            item.score += 4; item.reasons.append(f"due {d}")
        elif delta <= 7:
            item.score += 2; item.reasons.append(f"due {d} (this week)")
        else:
            item.reasons.append(f"due {d} (later)")

    if hits := _has(t, URGENT):
        item.score += 3; item.reasons.append("urgent: " + ", ".join(hits))
    if hits := _has(t, SOON):
        item.score += 2; item.reasons.append("soon: " + ", ".join(hits))
    if hits := _has(t, IMPORTANT):
        item.score += 2; item.reasons.append("high-stakes: " + ", ".join(hits))
    if _has(t, QUICK):
        item.quick = True
        item.score += 1; item.reasons.append("quick win")
    if hits := _has(t, CONSEQUENTIAL):
        item.approval = hits
    return item


def review(raw: str, today: date | None = None, source: str = "input") -> str:
    today = today or date.today()
    items, done = parse(raw)
    for it in items:
        score(it, today)

    active = [i for i in items if i.bucket == "next"]
    # stable sort: score desc, then original order
    active.sort(key=lambda i: (-i.score, i.line))
    top, rest = active[:3], active[3:]
    waiting = [i for i in items if i.bucket == "waiting"]
    defer = [i for i in items if i.bucket == "defer"]
    approval = [i for i in items if i.approval]
    unsignaled = [i for i in active if i.score == 0]

    def row(i: Item, num: str = "-") -> str:
        why = "; ".join(i.reasons) if i.reasons else "no deadline/importance signal — kept in your order"
        return f"{num} {i.text} — _{why}_ (L{i.line})"

    out = [f"# Productivity Review — {today.isoformat()}",
           "",
           f"Source: `{source}` · {len(items)} open items read · {done} completed items skipped",
           "",
           "## Top 3 Priorities"]
    out += [row(i, f"{k}.") for k, i in enumerate(top, 1)] or ["_None — no open items._"]
    out += ["", "## Next Actions"]
    out += [row(i) for i in rest] or ["_None._"]
    out += ["", "## Waiting / Blocked"]
    out += [row(i) for i in waiting] or ["_None._"]
    out += ["", "## Defer or Drop"]
    out += [row(i) for i in defer] or ["_None._"]
    out += ["", "## Needs Your Approval",
            "_These involve sending, paying, signing, deleting, etc. This review did not do them — they are yours to do or approve._"]
    out += [f"- {i.text} — _action: {', '.join(i.approval)}_ (L{i.line})" for i in approval] or ["_None._"]
    out += ["", "## Uncertain"]
    if unsignaled:
        out.append(f"- {len(unsignaled)} item(s) had no deadline or importance signal; their rank is a guess based on your original order. Add a date (YYYY-MM-DD) or word like `urgent` to sharpen it.")
    else:
        out.append("_None — every ranked item had at least one signal._")
    out += ["", "---", "Was this useful? **KEEP / CHANGE / DROP**", ""]
    return "\n".join(out)


__all__ = ["review", "parse", "score", "Item"]
