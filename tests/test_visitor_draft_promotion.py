#!/usr/bin/env python3
"""本番DBへの解説登録は、検証済み・ID別承認済みの同一版だけ許可する。"""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from scripts import visitor_draft_queue as queue


class PromotionGuardTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "data").mkdir()
        (self.root / "drafts/visitor-explanations").mkdir(parents=True)
        self.original = {"artworks": [
            {"id": "met-1", "facts": {"artist": "Painter 1"}},
            {"id": "aic-2", "facts": {"artist": "Painter 2"}, "curation": {"keep": True}},
        ]}
        self.write_json("data/artworks.json", self.original)
        self.write_json("data/visitor-explanation-approvals.json", {"approvals": []})
        self.add_draft("met-1")

    def write_json(self, relative, value):
        (self.root / relative).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def read_json(self, relative):
        return queue.load(self.root / relative)

    def add_draft(self, ident, content="pending", source="verified", rights="pending"):
        draft = {
            "id": ident,
            "visitor_explanation": {
                "language": "ja",
                "text": "これは作品について検証する独立した解説文です。",
                "source_urls": ["https://www.metmuseum.org/art/collection/search/1"],
                "review": {
                    "content_status": content,
                    "source_status": source,
                    "rights_status": rights,
                    "reviewed_on": "2026-10-22",
                },
            },
            "evidence": [{
                "claim": "この主張の根拠",
                "source_url": "https://www.metmuseum.org/art/collection/search/1",
                "source_location": "作品紹介",
                "checked_against_source": True,
            }],
        }
        self.write_json(f"drafts/visitor-explanations/{ident}.json", draft)
        return draft

    def verified(self, ident="met-1", rights="pending"):
        draft = self.add_draft(ident, content="verified", rights=rights)
        return draft

    def approve(self, ident="met-1"):
        draft = self.read_json(f"drafts/visitor-explanations/{ident}.json")
        db = self.read_json("data/visitor-explanation-approvals.json")
        db["approvals"].append({
            "id": ident,
            "visitor_sha256": queue.explanation_sha256(draft["visitor_explanation"]),
        })
        self.write_json("data/visitor-explanation-approvals.json", db)

    def promote(self, ids=("met-1",), approved=True):
        with redirect_stdout(io.StringIO()):
            return queue.promote(self.root, set(ids), approved)

    def assert_db_unchanged(self):
        self.assertEqual(self.read_json("data/artworks.json"), self.original)

    def test_pending_content_rejected_even_when_approved_in_manifest(self):
        self.approve()
        with self.assertRaisesRegex(ValueError, "両方がverified"):
            self.promote()
        self.assert_db_unchanged()

    def test_missing_individual_approval_rejected(self):
        self.verified()
        with self.assertRaisesRegex(ValueError, "個別承認"):
            self.promote()
        self.assert_db_unchanged()

    def test_changed_text_after_approval_rejected(self):
        self.verified()
        self.approve()
        draft = self.read_json("drafts/visitor-explanations/met-1.json")
        draft["visitor_explanation"]["text"] += "追記"
        self.write_json("drafts/visitor-explanations/met-1.json", draft)
        with self.assertRaisesRegex(ValueError, "再承認"):
            self.promote()
        self.assert_db_unchanged()

    def test_changed_sources_after_approval_rejected(self):
        self.verified()
        self.approve()
        draft = self.read_json("drafts/visitor-explanations/met-1.json")
        draft["visitor_explanation"]["source_urls"].append("https://example.org/source")
        self.write_json("drafts/visitor-explanations/met-1.json", draft)
        with self.assertRaisesRegex(ValueError, "再承認"):
            self.promote()
        self.assert_db_unchanged()

    def test_rights_needs_revision_rejected(self):
        self.verified(rights="needs_revision")
        self.approve()
        with self.assertRaisesRegex(ValueError, "権利"):
            self.promote()
        self.assert_db_unchanged()

    def test_explicit_flag_still_required(self):
        self.verified()
        self.approve()
        with self.assertRaisesRegex(ValueError, "承認後"):
            self.promote(approved=False)
        self.assert_db_unchanged()

    def test_promotes_only_approved_record_and_keeps_pending_rights(self):
        draft = self.verified()
        self.approve()
        self.assertEqual(self.promote(), 0)
        current = self.read_json("data/artworks.json")
        self.assertEqual(current["artworks"][0]["visitor_explanation"], draft["visitor_explanation"])
        self.assertEqual(current["artworks"][1], self.original["artworks"][1])
        self.assertEqual(current["artworks"][0]["visitor_explanation"]["review"]["rights_status"], "pending")

    def test_existing_explanation_is_never_overwritten(self):
        self.verified()
        self.approve()
        database = self.read_json("data/artworks.json")
        database["artworks"][0]["visitor_explanation"] = {"text": "既存の本文"}
        self.write_json("data/artworks.json", database)
        with self.assertRaisesRegex(ValueError, "上書き"):
            self.promote()
        self.assertEqual(self.read_json("data/artworks.json"), database)

    def test_batch_fails_without_partial_registration(self):
        self.verified()
        self.add_draft("aic-2", content="verified")
        self.approve("met-1")
        with self.assertRaisesRegex(ValueError, "個別承認"):
            self.promote(ids=("met-1", "aic-2"))
        self.assert_db_unchanged()

    def test_duplicate_approval_entries_rejected(self):
        self.verified()
        self.approve()
        db = self.read_json("data/visitor-explanation-approvals.json")
        db["approvals"].append(copy.deepcopy(db["approvals"][0]))
        self.write_json("data/visitor-explanation-approvals.json", db)
        with self.assertRaisesRegex(ValueError, "重複"):
            self.promote()
        self.assert_db_unchanged()

    def test_fingerprint_is_stable(self):
        draft = self.verified()
        first = queue.explanation_sha256(draft["visitor_explanation"])
        second = queue.explanation_sha256(self.read_json(
            "drafts/visitor-explanations/met-1.json"
        )["visitor_explanation"])
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_check_remains_valid_for_pending_drafts(self):
        errors, count = queue.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
