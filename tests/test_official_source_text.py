"""Executable regression tests for museum-source *text*, not merely source flags."""
import hashlib
import unittest
from unittest.mock import patch

from scripts import verify_official_source_text as checker


class SampleResponse:
    status = 200
    headers = {"Content-Type": "text/html; charset=utf-8"}

    def __init__(self, content):
        self.content = content

    def read(self, amount):
        return self.content[:amount]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class SourceTextChecks(unittest.TestCase):
    def setUp(self):
        self.official = "https://www.metmuseum.org/art/collection/search/12345678"
        self.claim = "この絵には家族の日常生活が描かれている。"
        self.quote = "The painting depicts an ordinary family gathered around a modest dinner table."
        self.art = {
            "id": "met-12345678",
            "source": {"artwork_url": self.official},
            "visitor_explanation": {"text": "室内の風景。" + self.claim, "source_urls": [self.official]},
        }
        self.audit = {"official_text_checks": [{
            "source_url": self.official,
            "source_section": "Artwork Overview",
            "source_excerpt": self.quote,
            "visitor_claim": self.claim,
        }]}
        self.html = ("<html><head><script>irrelevant other content</script></head>"
                     "<body><h1>Painting</h1><p>" + self.quote + "</p></body></html>").encode()

    def test_page_fetch_and_actual_quote_match(self):
        with patch.object(checker, "urlopen", return_value=SampleResponse(self.html)):
            digest = checker.online(self.audit, self.art)
        self.assertEqual(digest, hashlib.sha256(self.html).hexdigest())

    def test_self_asserted_source_flag_cannot_substitute_quote(self):
        self.audit["official_text_checks"] = []
        with self.assertRaisesRegex(ValueError, "at least one"):
            checker.offline(self.audit, self.art)

    def test_quote_missing_from_live_page_is_rejected(self):
        wrong_html = "<html><body>Nothing about this object in this page.</body></html>"
        with self.assertRaisesRegex(ValueError, "not found on fetched museum page"):
            checker.check_html(wrong_html, self.audit["official_text_checks"])

    def test_source_quote_only_in_script_is_not_proof(self):
        html = "<html><script>" + self.quote + "</script><body>Other page.</body></html>"
        with self.assertRaisesRegex(ValueError, "not found"):
            checker.check_html(html, self.audit["official_text_checks"])

    def test_api_cannot_masquerade_as_official_description(self):
        self.audit["official_text_checks"][0]["source_url"] = (
            "https://collectionapi.metmuseum.org/public/collection/v1/objects/12345678"
        )
        with self.assertRaisesRegex(ValueError, "official page"):
            checker.offline(self.audit, self.art)

    def test_claim_not_in_Japanese_text_fails(self):
        self.audit["official_text_checks"][0]["visitor_claim"] = "そこには雪が積もっている。"
        with self.assertRaisesRegex(ValueError, "not found in visitor text"):
            checker.offline(self.audit, self.art)

    def test_html_response_must_be_html(self):
        class WrongMime(SampleResponse):
            headers = {"Content-Type": "application/json"}
        with patch.object(checker, "urlopen", return_value=WrongMime(self.html)):
            with self.assertRaisesRegex(ValueError, "did not return HTML"):
                checker.online(self.audit, self.art)


if __name__ == "__main__":
    unittest.main()
