"""Registration must reject stale evidence and leave the catalog unchanged."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts import complete_artwork as complete

ROOT = Path(__file__).resolve().parents[1]
AUDIT = "docs/artwork-completion-audits/met-435997-2026-10-30.json"
PROPOSAL = "drafts/artwork-revisions/met-435997.json"
DRAFT = "drafts/visitor-explanations/met-435997.json"


class CompletionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for directory in ("data", "scripts"):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(ROOT / "README.md", self.root)
        for path in (AUDIT, PROPOSAL, DRAFT):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / path, target)
        # The checked-in fixture may already contain the completed artwork.
        db = self.read("data/artworks.json")
        art = next(a for a in db["artworks"] if a["id"] == "met-435997")
        if "completion" in art:
            art.pop("completion")
            art.pop("visitor_explanation")
            for change in reversed(self.read(PROPOSAL)["changes"]):
                target = art
                for key in change["path"][:-1]:
                    target = target[key]
                target[change["path"][-1]] = change["before"]
            self.write("data/artworks.json", db)
        self.before = (self.root / "data/artworks.json").read_bytes()

    def read(self, path):
        return json.loads((self.root / path).read_text())

    def write(self, path, obj):
        (self.root / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

    def rejected(self, fragment):
        with self.assertRaisesRegex(ValueError, fragment):
            complete.save(self.root, AUDIT)
        self.assertEqual((self.root / "data/artworks.json").read_bytes(), self.before)

    def test_save_without_approval_updates_one_record_and_preserves_legacy(self):
        (self.root / "data/visitor-explanation-approvals.json").unlink()
        complete.save(self.root, AUDIT)
        before = json.loads(self.before)
        after = self.read("data/artworks.json")
        changed = [a["id"] for a, b in zip(before["artworks"], after["artworks"]) if a != b]
        self.assertEqual(changed, ["met-435997"])
        art = next(a for a in after["artworks"] if a["id"] == "met-435997")
        self.assertEqual(art["visitor_explanation"], self.read(DRAFT)["visitor_explanation"])
        self.assertEqual(art["curation"]["emotions"], ["喜び"])
        self.assertEqual(complete.check(self.root)["完成"], 1)
        saved = (self.root / "data/artworks.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "already saved"):
            complete.save(self.root, AUDIT)
        self.assertEqual((self.root / "data/artworks.json").read_bytes(), saved)

    def test_hold_and_ineligible_and_remaining_are_rejected(self):
        original = self.read(AUDIT)
        for field in ("hold", "ineligible", "remaining"):
            with self.subTest(field=field):
                audit = copy.deepcopy(original)
                if field == "hold": audit["result"] = "HOLD"
                if field == "ineligible": audit["promotion"]["eligible"] = False
                if field == "remaining": audit["remaining"] = ["source unavailable"]
                self.write(AUDIT, audit)
                self.rejected("not eligible")

    def test_changed_draft_rejected(self):
        draft = self.read(DRAFT)
        draft["visitor_explanation"]["text"] += "改稿"
        self.write(DRAFT, draft)
        self.rejected("draft changed")

    def test_changed_proposal_rejected(self):
        proposal = self.read(PROPOSAL)
        proposal["changes"][0]["after"] = []
        self.write(PROPOSAL, proposal)
        self.rejected("evidence file changed")

    def test_missing_rights_or_material_issue_rejected(self):
        audit = self.read(AUDIT)
        audit["rights_check"]["unresolved_material_issues"] = ["licence unresolved"]
        self.write(AUDIT, audit)
        self.rejected("rights assessment")

    def test_source_url_without_direct_content_is_rejected(self):
        audit = self.read(AUDIT)
        audit["sources"][0]["observed"] = ""
        self.write(AUDIT, audit)
        self.rejected("unread visitor source")

    def test_unchecked_image_is_rejected(self):
        audit = self.read(AUDIT)
        audit["images"][0]["matches_registered_bytes"] = False
        self.write(AUDIT, audit)
        self.rejected("image mismatch")

    def test_catalog_version_change_is_rejected(self):
        db = self.read("data/artworks.json")
        art = next(a for a in db["artworks"] if a["id"] == "met-435997")
        art["facts"]["title_original"] += " changed"
        self.write("data/artworks.json", db)
        self.before = (self.root / "data/artworks.json").read_bytes()
        self.rejected("catalog version changed")

    def test_duplicate_id_is_rejected(self):
        db = self.read("data/artworks.json")
        db["artworks"].append(copy.deepcopy(db["artworks"][0]))
        self.write("data/artworks.json", db)
        self.before = (self.root / "data/artworks.json").read_bytes()
        self.rejected("catalog identity mismatch")

    def test_program_failure_does_not_write(self):
        with patch.object(complete, "validate_candidate", side_effect=ValueError("invalid structure")):
            self.rejected("invalid structure")

    def test_saved_content_and_audit_changes_are_detected(self):
        complete.save(self.root, AUDIT)
        db = self.read("data/artworks.json")
        art = next(a for a in db["artworks"] if a["id"] == "met-435997")
        art["visitor_explanation"]["text"] += "改稿"
        self.write("data/artworks.json", db)
        with self.assertRaisesRegex(ValueError, "saved artwork changed"):
            complete.check(self.root)

    def test_saved_audit_change_is_detected(self):
        complete.save(self.root, AUDIT)
        audit = self.read(AUDIT)
        audit["result"] = "HOLD"
        self.write(AUDIT, audit)
        with self.assertRaisesRegex(ValueError, "saved audit changed"):
            complete.check(self.root)

    def test_incomplete_ai_review_is_rejected(self):
        audit = self.read(AUDIT)
        audit["separate_pass_review"]["checks"] = []
        self.write(AUDIT, audit)
        self.rejected("incomplete review")

    def test_hold_status_applies_only_to_the_same_catalog_version(self):
        audit = self.read(AUDIT)
        audit["result"] = "HOLD"
        audit["remaining"] = ["primary source unavailable"]
        self.write(AUDIT, audit)
        self.assertEqual(complete.check(self.root)["保留"], 1)
        audit["version"]["artwork_record_sha256"] = "0" * 64
        self.write(AUDIT, audit)
        self.assertEqual(complete.check(self.root)["保留"], 0)

    def test_path_escape_is_rejected(self):
        audit = self.read(AUDIT)
        audit["proposal"]["path"] = "../outside.json"
        self.write(AUDIT, audit)
        self.rejected("path outside")


if __name__ == "__main__":
    unittest.main()
