import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.review import review, parse  # noqa: E402
from app.quality_gate import check  # noqa: E402

TODAY = date(2026, 11, 2)
EXAMPLES = sorted((ROOT / "examples").glob("*"))


class ReviewTests(unittest.TestCase):
    def test_examples_pass_gate(self):
        self.assertGreaterEqual(len(EXAMPLES), 3)
        for f in EXAMPLES:
            raw = f.read_text()
            res = check(raw, review(raw, TODAY, f.name))
            self.assertNotEqual(res["verdict"], "FAIL", f"{f.name}: {res['errors']}")

    def test_skips_done_headings_quotes(self):
        items, done = parse("# h\n- [x] done\n> quote\n- [ ] open\n")
        self.assertEqual([i.text for i in items], ["open"])
        self.assertEqual(done, 1)

    def test_label_lines_are_not_tasks(self):
        items, _ = parse("notes from standup:\n- real task\n")
        self.assertEqual([i.text for i in items], ["real task"])

    def test_overdue_and_dated_ranked_first(self):
        raw = "- tidy desk\n- file taxes 2026-10-30\n- prep demo tomorrow\n"
        out = review(raw, TODAY)
        top = out.split("## Top 3 Priorities")[1].split("##")[0]
        self.assertTrue(top.strip().startswith("1. file taxes"))

    def test_waiting_and_defer_buckets(self):
        out = review("- waiting on legal\n- someday learn rust\n- do thing\n", TODAY)
        self.assertIn("waiting on legal", out.split("## Waiting / Blocked")[1].split("##")[0])
        self.assertIn("someday learn rust", out.split("## Defer or Drop")[1].split("##")[0])

    def test_consequential_routed_to_approval(self):
        out = review("- pay invoice\n- send report to client\n", TODAY)
        appr = out.split("## Needs Your Approval")[1].split("##")[0]
        self.assertIn("pay invoice", appr)
        self.assertIn("send report to client", appr)

    def test_approving_spend_is_consequential(self):
        # Regression from viability run 1: "approve the vendor PO" was not gated.
        out = review("- approve the vendor PO for GPU capacity\n", TODAY)
        self.assertIn("approve the vendor PO", out.split("## Needs Your Approval")[1])

    def test_deterministic(self):
        raw = (ROOT / "examples" / "monday-work.md").read_text()
        self.assertEqual(review(raw, TODAY), review(raw, TODAY))

    def test_empty_input(self):
        res = check("", review("", TODAY))
        self.assertNotEqual(res["verdict"], "FAIL")


class GateCatchesBadOutput(unittest.TestCase):
    raw = "- write report\n- pay vendor invoice\n"

    def good(self):
        return review(self.raw, TODAY)

    def test_fabrication_fails(self):
        bad = self.good().replace("## Next Actions", "## Next Actions\n- invent a task — _x_ (L1)")
        self.assertEqual(check(self.raw, bad)["verdict"], "FAIL")

    def test_dropped_item_fails(self):
        bad = "\n".join(l for l in self.good().splitlines() if not l.startswith("1. "))
        self.assertEqual(check(self.raw, bad)["verdict"], "FAIL")

    def test_duplicate_fails(self):
        g = self.good()
        line = next(l for l in g.splitlines() if l.startswith("1. "))
        bad = g.replace("## Next Actions", "## Next Actions\n" + line.replace("1.", "-", 1))
        self.assertEqual(check(self.raw, bad)["verdict"], "FAIL")

    def test_missing_approval_fails(self):
        g = self.good()
        bad = "\n".join(l for l in g.splitlines() if not (l.startswith("- pay vendor") and "action:" in l))
        self.assertEqual(check(self.raw, bad)["verdict"], "FAIL")

    def test_action_claim_fails(self):
        bad = self.good() + "\nI sent the invoice to the vendor.\n"
        self.assertEqual(check(self.raw, bad)["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
