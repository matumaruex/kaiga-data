#!/usr/bin/env python3
"""Verify new-artwork source excerpts against the *actual official artwork page*.

Offline validation binds a short exact-source quotation to a specific claim in
the Japanese visitor explanation. Online validation fetches the museum page and
finds the quotation in its HTML text. This checks that the passage actually
exists at the cited URL, not that the interpretation is historically correct.
Older v2 audits are intentionally grandfathered; never rewrite past history.
"""
import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.request import Request, urlopen

MAX_BYTES = 6_000_000
MAX_EXCERPT = 220


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def normal(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    # HTML entities are resolved by the parser; curly apostrophes normalize here.
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(text.split())


class MainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignored = 0
        self.words = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.ignored += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.ignored:
            self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored and data.strip():
            self.words.append(data)


def offline(audit, art):
    """Reject evidence markers that don't bind a source excerpt to this work/text."""
    claims = audit.get("official_text_checks")
    require(isinstance(claims, list) and claims, "official text: at least one claim-to-source check required")
    official = art["source"]["artwork_url"]
    text = art["visitor_explanation"]["text"]
    allowed_urls = set(art["visitor_explanation"]["source_urls"])
    assert official.startswith(("https://www.metmuseum.org/art/collection/search/",
                                "https://www.artic.edu/artworks/"))
    seen = set()
    for i, check in enumerate(claims, 1):
        require(isinstance(check, dict) and set(check) == {
            "source_url", "source_section", "source_excerpt", "visitor_claim",
        }, f"official text check {i}: invalid structure")
        url = check["source_url"]
        require(url == official and url in allowed_urls,
                f"official text check {i}: must cite this artwork's official page (not API)")
        excerpt = check["source_excerpt"]
        require(isinstance(excerpt, str) and 35 <= len(excerpt.strip()) <= MAX_EXCERPT
                and len(excerpt.split()) >= 6,
                f"official text check {i}: substantive short source excerpt required")
        claim = check["visitor_claim"]
        require(isinstance(claim, str) and len(claim.strip()) >= 14
                and normal(claim) in normal(text),
                f"official text check {i}: cited Japanese claim not found in visitor text")
        loc = check["source_section"]
        require(isinstance(loc, str) and len(loc.strip()) >= 4,
                f"official text check {i}: missing museum-page section locator")
        key = (url, normal(excerpt), normal(claim))
        require(key not in seen, f"official text check {i}: duplicated evidence")
        seen.add(key)
    # Claim/quote correspondence is assessed by the independent substantive review;
    # this code only verifies the independently obtainable primary source text.
    return claims


def check_html(html, claims):
    """Pure check; can test failures without an internet request."""
    parser = MainText()
    parser.feed(html)
    page_text = normal(" ".join(parser.words))
    require(bool(page_text), "official text: official page contains no readable HTML text")
    for i, item in enumerate(claims, 1):
        require(normal(item["source_excerpt"]) in page_text,
                f"official text check {i}: quoted passage not found on fetched museum page")
    return hashlib.sha256(html.encode("utf-8")).hexdigest()


def online(audit, art):
    claims = offline(audit, art)
    # URL is constrained to the artwork's exact official domain/path by offline().
    url = art["source"]["artwork_url"]
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MuseumSourceCheck/1.0)",
        "Accept": "text/html",
    })
    with urlopen(request, timeout=35) as response:
        require(response.status == 200, f"official text: HTTP {response.status}")
        require("html" in response.headers.get("Content-Type", "").lower(),
                "official text: museum page did not return HTML")
        raw = response.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "official text: source page exceeds size limit")
    html = raw.decode("utf-8", errors="replace")
    digest = check_html(html, claims)
    print(f"PASS: {art['id']} {len(claims)} actual on-page excerpt(s) "
          f"at {url}; retrieved HTML SHA256 {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()
    import json
    def load(path):
        return json.loads(path.read_text(encoding="utf-8"))
    root = args.root.resolve()
    audit_path = (root / args.audit).resolve()
    require(audit_path.is_relative_to(root / "docs/artwork-completion-audits"),
            "audit path outside completion audits")
    audit = load(audit_path)
    require(audit.get("schema_version") == "artwork-v2-new-registration-2",
            "official-source verifier requires new audit v2")
    proposal = load(root / audit["candidate_path"])
    art = proposal["artwork"]
    require(audit["id"] == art["id"], "audit and artwork ID differ")
    online(audit, art) if args.online else offline(audit, art)
    print("PASS: official text checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, TypeError) as exc:
        sys.exit(f"FAIL: {exc}")
