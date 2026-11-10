"""Regression checks for small active handoff and preserved older snapshots."""
from datetime import datetime, timezone
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts import rotate_resume


ROOT = Path(__file__).resolve().parents[1]


class ResumeRotationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for relative in ("docs/resume-artwork-work.md", "docs/history/resume-updates.md"):
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    def new_status(self):
        return ("## 現在の状態（2026-11-11時点）\n\n"
                "- **完成登録：314作品**。最新mainを参照。\n"
                "- **次：315作品目**。未解決事項なし。\n")

    def test_initial_live_memo_is_short(self):
        self.assertEqual(rotate_resume.check(self.root), 0)

    def test_update_replaces_not_appends_and_saves_previous(self):
        before = (self.root / "docs/resume-artwork-work.md").read_text(encoding="utf-8")
        old_status, old_footer = rotate_resume.split_resume(before)
        self.assertTrue(rotate_resume.update(
            self.root, self.new_status(), datetime(2026, 11, 11, tzinfo=timezone.utc)))
        after = (self.root / "docs/resume-artwork-work.md").read_text(encoding="utf-8")
        self.assertIn("314作品", after)
        self.assertNotIn("313作品", after)
        self.assertIn(old_footer, after)
        journal = (self.root / "docs/history/resume-updates.md").read_text(encoding="utf-8")
        self.assertIn("313作品", journal)
        self.assertIn("2026-11-11", journal)
        self.assertIn(old_status.replace("## 現在の状態", "#### 保存前の状態", 1), journal)
        self.assertEqual(rotate_resume.check(self.root), 0)

    def test_identical_status_does_not_add_history(self):
        new = self.new_status()
        rotate_resume.update(self.root, new, datetime(2026, 11, 11, tzinfo=timezone.utc))
        journal = (self.root / "docs/history/resume-updates.md").read_bytes()
        self.assertFalse(rotate_resume.update(self.root, new))
        self.assertEqual(journal, (self.root / "docs/history/resume-updates.md").read_bytes())

    def test_rejects_multiple_current_sections_and_unbounded_text(self):
        with self.assertRaises(ValueError):
            rotate_resume.normalize_status(self.new_status() + "\n## 旧い再開地点\n")
        with self.assertRaises(ValueError):
            rotate_resume.normalize_status(self.new_status() + ("- 過去の作業記録\n" * 200))

    def test_check_rejects_grown_live_file(self):
        live = self.root / "docs/resume-artwork-work.md"
        s = live.read_text(encoding="utf-8")
        s = s.replace("\n## 過去の作業履歴\n", "\n" + "- 古い作業ログ\n" * 100 + "\n## 過去の作業履歴\n")
        live.write_text(s, encoding="utf-8")
        with self.assertRaises(ValueError):
            rotate_resume.check(self.root)


if __name__ == "__main__":
    unittest.main()
