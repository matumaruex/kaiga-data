"""Regression checks for retaining verified scope when legacy labels change."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from legacy_review_checkpoint import BASE, build


class MigrationCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base = self.root / BASE
        self.base.mkdir(parents=True)
        (self.base / "batches").mkdir()
        (self.root / "drafts/visitor-explanations").mkdir(parents=True)
        self.manifest = []
        self.audits = {}
        self.screens = {}
        for i in range(100):
            ident = f"met-{10000+i}"
            path = Path(f"drafts/visitor-explanations/{ident}.json")
            self.write(path, {"id": ident, "visitor_explanation": {"text": f"Description {i}"}})
            digest = hashlib.sha256((self.root / path).read_bytes()).hexdigest()
            batch = (i // 5) + 1
            self.manifest.append({"id": ident, "title": f"Legacy title {i}",
                                  "path": str(path), "sha256": digest, "batch": batch})
            self.audits.setdefault(batch, []).append({
                "id": ident, "draft_sha256": digest, "verdict": "no_text_issue_found",
                "sources": [{"url": "https://example.org/official", "location": "p1", "result": "read"}],
                "support_summary": "Checked stated claims", "findings": [],
            })
            self.screens.setdefault(batch, []).append({
                "id": ident, "draft_file_sha256": digest,
                "rights_status": "pending",
                "triage": "priority_rewrite_or_review" if i < 57 else "further_review_required",
                "reason": "Preliminary comparison; rights not cleared",
                "primary_source_url": "https://example.org/official",
                "source_scope": "Only first paragraph",
            })
        self.write(BASE / "manifest.json", {"total_items": 100, "items": self.manifest})
        for batch in range(1, 21):
            self.write(BASE / f"batches/{batch:02}.json",
                       {"batch": batch, "items": self.audits[batch]})
            self.write(BASE / f"text-rights-screen-{batch:02}.json",
                       {"batch": batch, "items": self.screens[batch]})

    def write(self, path, value):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")

    def test_all_original_results_are_preserved_without_promotion(self):
        snap = build(self.root)
        self.assertEqual(snap["counts"]["priority_originally_flagged"], 57)
        self.assertEqual(snap["counts"]["other_rights_screened"], 43)
        self.assertEqual(snap["counts"]["historical_content_audits_matching_current"], 100)
        self.assertEqual(snap["counts"]["rights_prescreens_matching_current"], 100)
        self.assertEqual(snap["counts"]["v2_complete"], 0)
        self.assertTrue(all(not r["eligible_for_auto_promotion"] for r in snap["artworks"]))

    def test_title_rename_does_not_reset_checks_when_id_and_text_match(self):
        self.manifest[0]["title"] = "Completely new title"
        self.write(BASE / "manifest.json", {"total_items": 100, "items": self.manifest})
        snap = build(self.root)
        self.assertTrue(snap["artworks"][0]["historical_content_audit"]["matches_current_draft"])
        self.assertTrue(snap["artworks"][0]["historical_rights_prescreen"]["matches_current_draft"])

    def test_changed_text_marks_old_checks_historical_not_completed(self):
        self.write(Path(self.manifest[0]["path"]),
                   {"id": self.manifest[0]["id"], "visitor_explanation": {"text": "Revised"}})
        snap = build(self.root)
        item = snap["artworks"][0]
        self.assertFalse(item["historical_content_audit"]["matches_current_draft"])
        self.assertFalse(item["historical_rights_prescreen"]["matches_current_draft"])
        self.assertFalse(item["eligible_for_auto_promotion"])
        self.assertEqual(snap["counts"]["rights_prescreens_matching_current"], 99)

    def test_future_followup_saved_with_exact_version(self):
        item = self.manifest[0]
        self.write(BASE / "rights-followups-v2/review-01.json", {
            "id": item["id"], "draft_sha256": item["sha256"],
            "result": "checked_for_similarity",
            "review_scope": "Direct comparison of paragraphs",
            "observations": "Independent Japanese summary checked; no copying in the reviewed portion",
            "source_urls": ["https://example.org/official"],
        })
        snap = build(self.root)
        self.assertEqual(snap["counts"]["current_draft_similarity_followups_saved"], 1)
        self.assertEqual(snap["counts"]["v2_complete"], 0)
        self.write(Path(item["path"]),
                   {"id": item["id"], "visitor_explanation": {"text": "Altered"}})
        snap = build(self.root)
        self.assertEqual(snap["counts"]["current_draft_similarity_followups_saved"], 0)
        self.assertFalse(snap["artworks"][0]["subsequent_similarity_followups"][0]
                         ["matches_current_draft"])

    def test_lost_batch_is_not_silently_ignored(self):
        (self.base / "text-rights-screen-02.json").unlink()
        with self.assertRaisesRegex(ValueError, "missing batches"):
            build(self.root)

    def test_mismatched_id_is_rejected(self):
        path = Path(self.manifest[0]["path"])
        self.write(path, {"id": "met-WRONG", "visitor_explanation": {"text": "bad"}})
        with self.assertRaisesRegex(ValueError, "ID does not match"):
            build(self.root)

    def test_rights_pending_cannot_be_relabelled_as_verified(self):
        self.screens[1][0]["rights_status"] = "verified"
        self.write(BASE / "text-rights-screen-01.json",
                   {"batch": 1, "items": self.screens[1]})
        with self.assertRaisesRegex(ValueError, "rights clearance"):
            build(self.root)


if __name__ == "__main__":
    unittest.main()
