"""Regression checks for v2 new-work registration (all examples are fabricated)."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts import add_artwork

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ArtworkExpansionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "data", self.root / "data")
        shutil.copytree(ROOT / "scripts", self.root / "scripts",
                        ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "README.md").write_bytes((ROOT / "README.md").read_bytes())
        db = add_artwork.load(self.root / "data/artworks.json")
        registry = add_artwork.load(self.root / "data/image-sources.json")
        original = next(a for a in db["artworks"] if a["id"].startswith("met-"))
        old_image = next(r for r in registry["records"] if r["id"] == original["id"])
        art = copy.deepcopy(original)
        image = copy.deepcopy(old_image)
        ident = "met-99999999"
        official = "https://www.metmuseum.org/art/collection/search/99999999"
        image_url = "https://images.metmuseum.org/CRDImages/ep/web-large/FICTIONALTEST.jpg"
        digest = "f" * 64
        art["id"] = image["id"] = ident
        art["source"]["artwork_id"] = 99999999
        art["source"]["artwork_url"] = official
        art["facts"]["artist"] = "Fictional Test Artist"
        art["facts"].pop("artist_canonical", None)
        art["facts"]["title_original"] = "Fictional new-work test only"
        art["image"]["image_id"] = ident + "-primary"
        art["image"]["display_url"] = image_url
        art["image"]["sha256"] = digest
        art["image"]["byte_length"] = 89000
        art["image"]["local_path"] = "/artworks/" + ident + ".jpg"
        art["image"]["source_registry_id"] = ident
        art["image"].pop("high_resolution", None)
        art.pop("completion", None)
        art["curation"]["evidence_url"] = official
        art["curation"]["meaning_basis"]["scholarly_interpretation"]["source_url"] = official
        # The fixture supplies made-up proofs ONLY to test rejecting malformed input.
        visitor = {
            "language": "ja",
            "text": "試験データです。実在する美術品の説明ではありません。",
            "source_urls": [official],
            "review": {
                "content_status": "verified", "source_status": "verified",
                "rights_status": "verified", "reviewed_on": "2026-11-10",
            },
        }
        art["visitor_explanation"] = visitor
        image["official_artwork_url"] = official
        image["accession_number"] = "2026.99.1"
        image["in_shared_catalog"] = True
        image["image_source"]["type"] = "met_open_access"
        image["image_source"]["official_image_page"] = official
        image["image_source"]["verified_download_url"] = image_url
        image["image_source"]["sha256"] = digest
        image["image_source"]["byte_length"] = 89000
        image["image_source"].pop("high_resolution", None)
        self.ident = ident
        self.proposal_path = self.root / "drafts/artwork-additions" / (ident + ".json")
        self.draft_path = self.root / "drafts/visitor-explanations" / (ident + ".json")
        self.audit_path = self.root / "docs/artwork-completion-audits" / (ident + "-2026-11-10.json")
        write_json(self.proposal_path, {
            "schema_version": "artwork-addition-proposal-v1",
            "id": ident, "artwork": art, "image_record": image
        })
        write_json(self.draft_path, {
            "id": ident,
            "visitor_explanation": visitor,
            "evidence": [{
                "claim": "Only a synthetic test fixture",
                "source_url": official, "source_location": "Test fixture entry",
                "checked_against_source": True,
            }],
        })
        rights_url = image["image_source"]["license_url"]
        evidence = [
            {"url": url, "location": "Synthetic fixture source",
             "finding": "Synthetic test only", "checked_against_source": True}
            for url in dict.fromkeys([official, rights_url])
        ]
        self.audit = {
            "schema_version": "artwork-v2-new-registration-1",
            "id": ident,
            "result": "PASS", "unresolved_material_issues": [],
            "candidate_path": str(self.proposal_path.relative_to(self.root)),
            "candidate_sha256": add_artwork.file_sha(self.proposal_path),
            "draft_path": str(self.draft_path.relative_to(self.root)),
            "draft_sha256": add_artwork.file_sha(self.draft_path),
            "baseline": {
                "artworks_sha256": add_artwork.file_sha(self.root / "data/artworks.json"),
                "image_registry_sha256": add_artwork.file_sha(self.root / "data/image-sources.json"),
            },
            "source_evidence": evidence,
            "rights": {
                "artwork": {
                    "verified": True, "public_domain": True,
                    "finding": "Synthetic fixture", "source_url": official,
                },
                "image": {
                    "verified": True, "permitted_for_site_use": True,
                    "finding": "Synthetic fixture", "source_url": rights_url,
                },
                "text": {
                    "verified": True, "independent_japanese_prose": True,
                    "finding": "Synthetic fixture", "source_url": official,
                },
            },
            "separate_pass_review": {
                "result": "PASS", "method": "Synthetic test",
                "limitations": "No external source or image inspected by this unit test",
                "areas": sorted(add_artwork.REVIEW_AREAS),
            },
            "image_evidence": [{
                "kind": "display", "url": image_url,
                "sha256": digest, "byte_length": 89000,
                "download_status": 200,
                "full_bytes_sha256_checked": True,
                "image_subject_visually_compared": True,
                "observation": "Synthetic fixture; never real-world proof",
                "checked_on": "2026-11-10",
            }],
        }
        self.flush_audit()

    def flush_audit(self):
        write_json(self.audit_path, self.audit)

    def test_preview_and_save_preserve_all_old_records(self):
        previous = (self.root / "data/artworks.json").read_bytes()
        outputs = add_artwork.candidate_files(self.root, self.audit_path)
        add_artwork.validate_candidate(self.root, outputs)
        self.assertEqual((self.root / "data/artworks.json").read_bytes(), previous)
        add_artwork.save_files(self.root, outputs)
        additions = add_artwork.check(self.root)
        self.assertEqual(additions, 1)
        saved = add_artwork.load(self.root / "data/artworks.json")["artworks"]
        self.assertEqual(len(saved), 301)
        self.assertEqual(json.loads(previous)["artworks"], saved[:-1])
        self.assertIn("**v2完成登録：301作品**",
                      (self.root / "README.md").read_text(encoding="utf-8"))
        self.audit["baseline"]["artworks_sha256"] = add_artwork.file_sha(
            self.root / "data/artworks.json")
        self.audit["baseline"]["image_registry_sha256"] = add_artwork.file_sha(
            self.root / "data/image-sources.json")
        self.flush_audit()
        with self.assertRaisesRegex(ValueError, "already registered"):
            add_artwork.candidate_files(self.root, self.audit_path)

    def test_rights_and_visual_review_must_both_pass(self):
        self.audit["rights"]["image"]["permitted_for_site_use"] = False
        self.flush_audit()
        with self.assertRaisesRegex(ValueError, "rights must be assessed"):
            add_artwork.candidate_files(self.root, self.audit_path)
        self.audit["rights"]["image"]["permitted_for_site_use"] = True
        self.audit["image_evidence"][0]["image_subject_visually_compared"] = False
        self.flush_audit()
        with self.assertRaisesRegex(ValueError, "visual evidence missing"):
            add_artwork.candidate_files(self.root, self.audit_path)

    def test_source_changes_or_missing_separate_review_fail_closed(self):
        self.audit["separate_pass_review"]["areas"].remove("identity")
        self.flush_audit()
        with self.assertRaisesRegex(ValueError, "separate source"):
            add_artwork.candidate_files(self.root, self.audit_path)
        self.audit["separate_pass_review"]["areas"].append("identity")
        self.audit["baseline"]["artworks_sha256"] = "0" * 64
        self.flush_audit()
        with self.assertRaisesRegex(ValueError, "database changed"):
            add_artwork.candidate_files(self.root, self.audit_path)

    def test_undocumented_candidate_modification_rejected(self):
        proposal = add_artwork.load(self.proposal_path)
        proposal["artwork"]["facts"]["title_original"] = "Edited after review"
        write_json(self.proposal_path, proposal)
        with self.assertRaisesRegex(ValueError, "candidate changed"):
            add_artwork.candidate_files(self.root, self.audit_path)


if __name__ == "__main__":
    unittest.main()
